"""Independent verifier checks; synthetic arrays are for unit checks only."""
import csv, difflib, hashlib, importlib.util, json, platform, sys, zipfile
from pathlib import Path
import numpy as np
import torch
from PIL import Image
ROOT=Path.cwd(); OUT=ROOT/'results/verification/independent-20261029'
checks=[]
def passed(name, **details):
    checks.append({'check':name,'status':'passed',**details}); print('PASS',name,flush=True)
def sha(data): return hashlib.sha256(data).hexdigest()
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'src'/name/(name+'.py'))
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
p1,p2,p3=map(load,['p1','p2','p3'])
versions={str(f.relative_to(ROOT)):sha(f.read_bytes()) for f in (ROOT/'src').glob('p*/*.py')}
(OUT/'checked-source-sha256.json').write_text(json.dumps(versions,indent=2))
with zipfile.ZipFile(ROOT/'requirements/code_source(2).zip') as z:
    edit_count=0; data_count=0; diffs={}
    for p in ['p1','p2','p3']:
        old=z.read(f'code_source/{p}/{p}.py').decode().splitlines(keepends=True)
        new=(ROOT/f'src/{p}/{p}.py').read_text().splitlines(keepends=True)
        changed=[x for x in difflib.SequenceMatcher(None,old,new).get_opcodes() if x[0]!='equal']
        for tag,a,b,c,d in changed:
            assert tag=='replace' and b-a==1 and old[a].strip().startswith('raise NotImplementedError'),(p,tag,old[a:b])
        edit_count+=len(changed)
        diffs[p]=''.join(difflib.unified_diff(old,new,fromfile='teacher',tofile='completed'))
        assert z.read(f'code_source/{p}/requirements.txt')==(ROOT/f'src/{p}/requirements.txt').read_bytes()
    assert edit_count==8
    for info in z.infolist():
        if info.filename.startswith('code_source/') and '/data/' in info.filename and not info.is_dir() and not info.filename.endswith('.DS_Store'):
            relative=info.filename.removeprefix('code_source/')
            assert z.read(info.filename)==(ROOT/'src'/relative).read_bytes(),relative
            data_count+=1
    (OUT/'todo-only.diff').write_text('\n'.join(diffs.values()))
passed('Only eight TODO raise statements replaced; all other framework text/dependencies unchanged', data_files_identical=data_count)
manifest=json.loads((ROOT/'results/input-manifest.json').read_text())
for name,meta in manifest.items():
    raw=(ROOT/name).read_bytes(); assert len(raw)==meta['size'] and sha(raw)==meta['sha256'], name
passed('Recorded input manifest hashes match actual files', files=len(manifest))
# Independent ridge oracle: solve augmented overdetermined system by least squares.
rng=np.random.default_rng(119)
for m,d in [(1,1),(3,7),(19,4)]:
    X=rng.normal(size=(m,d)); X[:,0]=1; y=rng.normal(size=m)
    for lam in [1e-5,.01,1.,100.]:
        expected=np.linalg.lstsq(np.r_[X,np.sqrt(m*lam)*np.eye(d)],np.r_[y,np.zeros(d)],rcond=None)[0]
        np.testing.assert_allclose(p1.fit_ridge_final(X,y,lam),expected,rtol=1e-8,atol=1e-9)
np.testing.assert_allclose(p1.fit_ridge_final(np.ones((5,1)),np.full(5,6.),2.),[2.],rtol=1e-13)
passed('Ridge mean scaling, intercept penalty, underdetermined/full-rank cases against augmented least squares')
train,test=p1.load_data(); x,y=train.T
folds=[[6,0],[3,9],[2,1],[4,8],[5,7]]
assert p1.FIXED_FOLDS.tolist()==folds
assert sorted(sum(folds,[]))==list(range(10))
X=np.column_stack([x**j for j in range(9)])
cv=[]
for lam in p1.LAMBDAS:
    row=[]
    for valid in folds:
        ids=[j for j in range(10) if j not in valid]
        A=X[ids]; b=y[ids]
        theta=np.linalg.lstsq(np.r_[A,np.sqrt(8*lam)*np.eye(9)],np.r_[b,np.zeros(9)],rcond=None)[0]
        row.append(float(np.sum((X[valid]@theta-y[valid])**2)/2))
    cv.append(row)
best,actual,_=p1.cross_validate(x,y)
np.testing.assert_allclose(actual,cv,rtol=1e-10,atol=1e-12)
assert best==.01
# Deliberately shuffle supplied records; three exact ties must select smallest candidate.
records=[(c,f,np.array([2.,5.]),np.array([4.,1.])) for c in range(3) for f in range(5)]
rng.shuffle(records)
best_tie,score=p1.score_and_select_cv(records,[.001,.1,3.])
assert best_tie==.001; np.testing.assert_array_equal(score,np.full((3,5),10.))
passed('All 80 held-out fold scores independently recomputed; fixed row IDs and exact tie', selected_lambda=best,max_abs_difference=float(np.max(np.abs(actual-cv))))
# P2 all image ordering and normalization, plus deliberately non-contiguous synthetic arrays.
images,paths=p2.load_images(); X=p2.build_data_matrix(images)
assert X.shape==(10304,400)
for i,path in enumerate(paths):
    assert path.parent.name==f's{i//10+1}' and path.stem==str(i%10+1)
    np.testing.assert_array_equal(X[:,i],np.asarray(Image.open(path),dtype=float).ravel(order='C')/255.)
synthetic=np.arange(60.).reshape(5,3,4)[:,:,::-1]
np.testing.assert_array_equal(p2.build_data_matrix(synthetic),np.stack([a.ravel(order='C') for a in synthetic],axis=1))
mu,U,s=p2.pca(X)
assert mu.shape==(10304,1) and U.shape==(10304,400) and s.shape==(400,)
np.testing.assert_allclose(mu,np.sum(X,axis=1,keepdims=True)/400,rtol=1e-14,atol=1e-15)
np.testing.assert_allclose(U.T@U,np.eye(400),atol=1e-12,rtol=1e-12)
assert np.all(np.diff(s)<=0)
errs={}
for k in [20,100,400]:
    coords,rebuilt=p2.project_and_reconstruct(X,mu,U,k)
    np.testing.assert_allclose(coords,U[:,:k].T@(X-mu),rtol=1e-12,atol=1e-12)
    residual=np.mean((rebuilt-X)**2); tail=np.sum(s[k:]**2)/X.size
    np.testing.assert_allclose(residual,tail,rtol=1e-10,atol=1e-20)
    errs[k]={'mse':float(residual),'tail_energy_mse':float(tail),'min_reconstruction':float(rebuilt.min()),'max_reconstruction':float(rebuilt.max())}
np.testing.assert_allclose(rebuilt,X,rtol=1e-11,atol=1e-11)
assert errs[20]['max_reconstruction']>1 # proves returned values were not clipped
passed('All 400 faces C-order/normalization/order; thin centered SVD; orthonormality; unclipped projection and tail energy', errors=errs)
# P3 exact leaf structure, raw scores, batch dimensions and affine equivalence.
p3.configure_cpu(); torch.manual_seed(119)
for name,expected,count in [('A',[torch.nn.Linear],7850),('B',[torch.nn.Linear]*2,50890),('C',[torch.nn.Linear,torch.nn.ReLU,torch.nn.Linear],50890)]:
    model=p3.build_model(name).double()
    leaves=[a for a in model.modules() if not list(a.children())]
    assert [type(a) for a in leaves]==expected
    assert all(a.bias is not None for a in leaves if isinstance(a,torch.nn.Linear))
    assert sum(a.numel() for a in model.parameters())==count
    for batch in [0,1,17]: assert model(torch.randn(batch,784,dtype=torch.float64)).shape==(batch,10)
    with torch.no_grad():
        for param in model.parameters(): param.zero_()
        leaves[-1].bias.fill_(-3)
    torch.testing.assert_close(model(torch.zeros(2,784,dtype=torch.float64)),torch.full((2,10),-3.,dtype=torch.float64),rtol=0,atol=0)
model=p3.build_model_b().double(); a,b=list(model.children()); t=torch.randn(13,784,dtype=torch.float64)
torch.testing.assert_close(model(t),t@(b.weight@a.weight).T+b.weight@a.bias+b.bias,rtol=1e-11,atol=1e-12)
# Use known parameter assignments to expose C's piecewise rather than affine response.
c=p3.build_model_c().double()
with torch.no_grad():
    for param in c.parameters(): param.zero_()
    c[0].weight[0,0]=1; c[2].weight[0,0]=1
z=torch.zeros(1,784,dtype=torch.float64); z[0,0]=1
assert (c(z)+c(-z)-2*c(z*0))[0,0].item()==1
passed('P3 layer types/biases/counts; empty and nonempty batches; raw negative logits; B affine collapse; C nonlinearity')
data,splits=p3.load_data()
assert {k:len(v) for k,v in splits.items()}=={'train':6000,'validation':2000,'test':2000}
assert not set(splits['train'])&set(splits['validation'])
for key,(pixels,labels) in data.items():
    assert pixels.dtype==torch.float32 and pixels.min()>=0 and pixels.max()<=1
    assert len(set(splits[key]))==len(splits[key])
    assert torch.bincount(labels).tolist()==([600]*10 if key=='train' else [200]*10)
passed('P3 fixed class-balanced disjoint train/validation split; official test subset; normalization',split_sizes={k:len(v) for k,v in splits.items()})
# Fresh run comparisons: exact-byte equality is expected with same CPU, seed and pins.
original=ROOT/'results/run-20261029'
for p,files in {'p1':['summary.json','cross_validation.csv','validation.png','fits.png','data_target.png'],'p2':['summary.json','mse.csv','eigenfaces.png','reconstruction.png'],'p3':['summary.csv','A_history.csv','B_history.csv','C_history.csv','selection_before_test.json','architecture_curves.png']}.items():
    for f in files: assert (OUT/p/f).read_bytes()==(original/p/f).read_bytes(),(p,f)
passed('All numerical output tables/histories and six requested/generated plots reproduce byte-for-byte')
for name in ['A','B','C']:
    with (OUT/f'p3/{name}_history.csv').open() as f: history=list(csv.DictReader(f))
    assert len(history)==31
    best=min(history[1:],key=lambda r:float(r['validation_ce']))
    manifest=json.loads((OUT/'p3/manifest.json').read_text())
    row=next(r for r in manifest['rows'] if r['model']==name)
    assert row['best_epoch']==int(best['epoch']) and row['validation_ce']==float(best['validation_ce'])
assert manifest['selection']['selected_model']=='C' and manifest['selection']['test_metrics_used'] is False
assert manifest['epochs']==30 and manifest['batch_size']==128 and manifest['learning_rate']==.1 and manifest['momentum']==.9 and manifest['weight_decay']==0
assert versions=={str(f.relative_to(ROOT)):sha(f.read_bytes()) for f in (ROOT/'src').glob('p*/*.py')}
passed('Checkpoint minima among trained epochs; C selected by validation; supplied training settings; input code stable')
(OUT/'checks.json').write_text(json.dumps({'executor':'/root/verifier','python':sys.version,'platform':platform.platform(),'checks':checks},indent=2))
print('ALL INDEPENDENT CHECKS PASSED')
