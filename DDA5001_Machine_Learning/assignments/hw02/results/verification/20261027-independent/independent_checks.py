from pathlib import Path
import sys, json, hashlib, zipfile, importlib.util, csv, datetime
import numpy as np
from numpy.polynomial.legendre import leggauss,legval,legvander
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from threadpoolctl import threadpool_limits
OUT=Path(__file__).resolve().parent; BASE=OUT.parents[2]
checks={}
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
a2=load('ind_alg2',OUT/'src/p2/algorithms.py');a3=load('ind_alg3',OUT/'src/p3/algorithms.py')
sys.path.insert(0,str(OUT/'src/p2')); f2=load('ind_f2',OUT/'src/p2/framework.py');sys.path.pop(0)
sys.modules['algorithms']=a3;f3=load('ind_f3',OUT/'src/p3/framework.py');sys.modules.pop('algorithms')
def record(name,**data):checks[name]={'passed':True,**data}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Source fidelity and originals, from actual ZIP bytes (skip Apple metadata).
originals={}
with zipfile.ZipFile(BASE/'code_source(1).zip') as z:
 for name in z.namelist():
  if not name.startswith('code_source/') or not name.endswith(('.py','.txt')):continue
  rel=name[len('code_source/'):];current=BASE/'src'/rel
  unchanged=z.read(name)==current.read_bytes()
  originals[rel]={'original_sha256':hashlib.sha256(z.read(name)).hexdigest(),'current_sha256':sha(current),'unchanged':unchanged}
  if not rel.endswith('algorithms.py'):assert unchanged, rel
assert len(originals)==9
(OUT/'original-comparison.json').write_text(json.dumps(originals,indent=2)+'\n')
hashes=json.loads((OUT/'input-hashes.json').read_text())
for p,h in hashes.items():
 if p.startswith('src/'):assert sha(BASE/p)==h,p
record('source_fidelity',teacher_text_files=9,unchanged_framework_runner_tests_requirements=7,source_snapshot_unchanged=True)
# Stable finite logits, ties, singleton class and immutable noncontiguous views.
logits=np.array([[1e100,-1e100,0.],[0.,0.,0.],[-1e100,-1e100,-1e100]])
logits.setflags(write=False);Y=np.eye(3)[[1,2,0]];Y.setflags(write=False)
p=a2.softmax(logits); np.testing.assert_allclose(p.sum(1),1.,atol=1e-15,rtol=0)
assert np.isfinite(a2.cross_entropy(logits,Y));np.testing.assert_allclose(a2.cross_entropy(logits,Y),(2e100+2*np.log(3))/3,rtol=1e-15)
assert a2.cross_entropy(np.ones((5,1))*1000,np.ones((5,1)))==0
rng=np.random.default_rng(20261027);maxdiff=0.
for n,d,k in [(1,1,1),(3,2,2),(7,4,5),(13,5,3)]:
 X=rng.normal(size=(n,d*2))[:,::2];T=rng.normal(size=(d,k));Y=np.eye(k)[rng.integers(k,size=n)]
 for v in (X,T,Y):v.setflags(write=False)
 G=a2.gradient(T,X,Y);num=np.empty_like(T);h=1e-6
 for ix in np.ndindex(T.shape):
  plus=T.copy();minus=T.copy();plus[ix]+=h;minus[ix]-=h
  num[ix]=(a2.cross_entropy(X@plus,Y)-a2.cross_entropy(X@minus,Y))/(2*h)
 diff=float(np.max(np.abs(G-num)));maxdiff=max(maxdiff,diff)
 np.testing.assert_allclose(G,num,atol=2e-8,rtol=1e-6)
 perm=rng.permutation(n);np.testing.assert_allclose(G,a2.gradient(T,X[perm],Y[perm]),atol=1e-14,rtol=1e-14)
 np.testing.assert_allclose(G.sum(1),0,atol=1e-14,rtol=0)
record('p2_generalized_gradient_and_stability',random_shape_cases=4,max_gradient_finite_difference=maxdiff,gradient_atol=2e-8,finite_extreme_logits=1e100,readonly_noncontiguous_inputs=True,single_class=True)
# Independent nonlinear update oracle prevents evaluation-point errors hidden by linear G.
T=rng.normal(size=(4,3));P=rng.normal(size=(4,3));T.setflags(write=False);P.setflags(write=False)
G=lambda a:np.sin(a)+a*a
for k in (1,2,3,999):
 calls=[]
 def captured(a):calls.append(a.copy());return G(a)
 W=T+(k-1)/(k+2)*(T-P); actual=a2.nesterov_step(T,P,.05,k,captured)
 assert len(calls)==1;np.testing.assert_array_equal(calls[0],W);np.testing.assert_allclose(actual,W-.05*G(W),atol=1e-14,rtol=0)
np.testing.assert_allclose(a2.momentum_step(T,P,.05,.9,G),T-.05*G(T)+.9*(T-P),atol=1e-14,rtol=0)
record('p2_nonlinear_update_oracle',nesterov_steps=[1,2,3,999],atol=1e-14,gradient_calls_per_step=1)
# Reconstruct scaling/split without framework and compare all arrays on official inputs.
dataset_checks={}
for name in ('digits','dry_bean'):
 X,Y,V,Z,m=f2.prepare_dataset(name,BASE/'data')
 if name=='digits': raw,labels=load_digits(return_X_y=True)
 else:
  with (BASE/'data/dry_bean.csv').open() as stream: rows=list(csv.DictReader(stream))
  raw=np.array([[float(r[key]) for key in f2.BEAN_FEATURES] for r in rows]);labels=np.array([f2.BEAN_CLASSES.index(r['Class']) for r in rows])
 seen=set();keep=[]
 for j,row in enumerate(raw):
  key=row.tobytes()
  if key not in seen:seen.add(key);keep.append(j)
 raw=raw[keep];labels=labels[keep]
 it,iv=train_test_split(np.arange(len(labels)),test_size=.2,random_state=666,stratify=labels)
 mean=raw[it].mean(0);std=raw[it].std(0);std[std==0]=1
 np.testing.assert_array_equal(X[:,:-1],(raw[it]-mean)/std);np.testing.assert_array_equal(V[:,:-1],(raw[iv]-mean)/std)
 np.testing.assert_array_equal(Y,np.eye(Y.shape[1])[labels[it]]);np.testing.assert_array_equal(Z,np.eye(Y.shape[1])[labels[iv]])
 assert np.all(X[:,-1]==1) and np.all(V[:,-1]==1)
 dataset_checks[name]={'train':len(it),'test':len(iv),'duplicates_removed':m['duplicates_removed'],'parameter_shape':m['parameter_shape']}
record('p2_dataset_independent_reconstruction',datasets=dataset_checks,csv_sha256=sha(BASE/'data/dry_bean.csv'))
# Instrument a full 1000-update tiny run, perturb all test labels, require identical trained models.
X=rng.normal(size=(19,4));Y=np.eye(3)[rng.integers(3,size=19)];V=rng.normal(size=(8,4));Z=np.eye(3)[rng.integers(3,size=8)]
counts={}
class Wrapped:
 softmax=staticmethod(a2.softmax);cross_entropy=staticmethod(a2.cross_entropy);gd_step=staticmethod(a2.gd_step);momentum_step=staticmethod(a2.momentum_step);nesterov_step=staticmethod(a2.nesterov_step)
 def gradient(self,T,train,labels):
  assert train is X and labels is Y
  self.calls+=1;return a2.gradient(T,train,labels)
with threadpool_limits(limits=1):
 for method in f2.METHODS:
  wrapped=Wrapped();wrapped.calls=0;T,H=f2.train_one(method,X,Y,V,Z,wrapped);assert wrapped.calls==1000
  wrapped.calls=0;U,J=f2.train_one(method,X,Y,V*9,np.roll(Z,1,axis=1),wrapped);assert wrapped.calls==1000
  np.testing.assert_array_equal(T,U)
  assert [a['iteration'] for a in H]==list(range(0,1001,5))
  assert all(a['train_loss']==b['train_loss'] for a,b in zip(H,J));counts[method]=1000
record('p2_no_test_leakage_and_update_count',gradient_calls=counts,perturbed_test_inputs_and_labels=True,trained_parameters_bitwise_equal=True)
# Independent quadrature for randomized batched error, differing tails and singleton batches.
nodes,weights=leggauss(80);maxquad=0.;maxfit=0.
for deg,target_deg,batch in [(0,0,1),(2,50,3),(10,1,4),(10,50,1),(50,2,2)]:
 W=rng.normal(size=(deg+1,batch));C=rng.normal(size=(target_deg+1,batch));W.setflags(write=False);C.setflags(write=False)
 analytic=a3.population_error(W,C);quadrature=np.array([sum(weights*(legval(nodes,W[:,j])-legval(nodes,C[:,j]))**2)/2 for j in range(batch)])
 assert analytic.shape==(batch,);maxquad=max(maxquad,float(np.max(np.abs(analytic-quadrature))))
 np.testing.assert_allclose(analytic,quadrature,atol=1e-10,rtol=1e-10)
 np.testing.assert_array_equal(analytic,a3.population_error(C,W))
 for j in range(batch):np.testing.assert_allclose(analytic[j],a3.population_error(W[:,j],C[:,j]),atol=1e-14,rtol=1e-14)
for degree in (0,2,10):
 x=np.cos(np.pi*(np.arange(degree+1)+.5)/(degree+1));A=legvander(x,degree);truth=rng.normal(size=(degree+1,3));y=A@truth
 A.setflags(write=False);y.setflags(write=False);fit=a3.fit_polynomial(A,y);error=float(np.max(np.abs(fit-truth)));maxfit=max(maxfit,error)
 np.testing.assert_allclose(fit,truth,atol=1e-11,rtol=0)
record('p3_quadrature_tails_batches_and_minimal_full_rank_fit',quadrature_cases=5,max_quadrature_difference=maxquad,quadrature_tolerance=1e-10,max_fit_coefficient_difference=maxfit,fit_tolerance=1e-11,readonly_inputs=True)
# All original full-experiment numeric outputs vs fresh clean-room outputs.
compare={}
for problem in (2,3):
 main=BASE/f'results/run-20261027/p{problem}';fresh=OUT/f'p{problem}-full';files={}
 for p in sorted(main.iterdir()):
  if p.suffix=='.csv':
   # Same pinned libraries, host and seed: bitwise CSV equality is warranted.
   assert p.read_bytes()==(fresh/p.name).read_bytes(),p.name;files[p.name]={'byte_equal':True}
  if p.suffix=='.npy':
   a,b=np.load(p),np.load(fresh/p.name);np.testing.assert_array_equal(a,b);files[p.name]={'shape':list(a.shape),'exact_equal':True}
  if p.suffix=='.npz':
   with np.load(p) as a,np.load(fresh/p.name) as b:
    assert a.files==b.files
    for key in a.files:np.testing.assert_array_equal(a[key],b[key])
    files[p.name]={key:{'shape':list(a[key].shape),'exact_equal':True} for key in a.files}
  if p.name=='summary.json':assert json.loads(p.read_text())==json.loads((fresh/p.name).read_text())
 original=json.loads((main/'manifest.json').read_text());reproduced=json.loads((fresh/'manifest.json').read_text())
 original.pop('elapsed_seconds',None);reproduced.pop('elapsed_seconds',None);assert original==reproduced
 compare[f'p{problem}']={'files':files,'manifest_equal_except_elapsed_seconds':True}
with np.load(OUT/'p3-full/trial_values.npz') as a,np.load(OUT/'p3-full/grid_means.npz') as b:
 assert a['rho_q'].shape==(1000,21,50) and a['rho_v'].shape==(1000,21,41)
 for key in a.files:assert np.isfinite(a[key]).all()
 np.testing.assert_array_equal(a['rho_q'].mean(0),b['mean_q']);np.testing.assert_array_equal(a['rho_v'].mean(0),b['mean_v'])
 np.testing.assert_array_equal(a['rho_q'][:,:,19],a['rho_v'][:,:,2])
 np.testing.assert_array_equal(a['risk10_q20']-a['risk2_q20'],a['rho_q'][:,:,19])
 record('p3_all_trials_mean_and_paired_grid_overlap',shape_q=list(a['rho_q'].shape),shape_v=list(a['rho_v'].shape),total_cell_trial_observations=1911000,all_finite=True,means_exact=True,overlap_exact=True,max_raw_rho_q=float(a['rho_q'].max()),max_raw_rho_v=float(a['rho_v'].max()))
record('full_clean_room_reproduction',comparisons=compare,all_numeric_arrays_and_csvs_bitwise_equal=True)
(OUT/'independent-checks.json').write_text(json.dumps({'executor':'/root/verifier','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'all_passed':True},indent=2)+'\n')
print(json.dumps(checks,indent=2))
