from run import ROOT,OUT,run
import subprocess,time,json,datetime
rows=[]
for n in range(1,11):
 args=['psql','-X','-q','-A','-t','-v','ON_ERROR_STOP=1','-d','proj1_verify_20261028_checked','-c',f"SET statement_timeout='120s'; SELECT * FROM q{n}"]
 t=time.monotonic();p=subprocess.run(args,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True,cwd=ROOT)
 rows.append(dict(query=f'q{n}',argv=args,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-t,exit=p.returncode,stderr=p.stderr,output='Full rows retrieved by psql and discarded to /dev/null, no COUNT optimization'))
 assert p.returncode==0,p.stderr
(OUT/'full-retrieval.json').write_text(json.dumps(rows,indent=2)); print([(x['query'],round(x['seconds'],3)) for x in rows])
run('subject-identity',['psql','-X','-d','proj1_verify_20261028_checked','-c',"SELECT count(*) AS multi_version_codes FROM (SELECT code FROM subjects GROUP BY code HAVING count(*)>1)x; SELECT count(*) AS multiple_offerings_per_code_term FROM (SELECT s.code,c.semester FROM courses c JOIN subjects s ON s.id=c.subject GROUP BY s.code,c.semester HAVING count(*)>1)x;"])
