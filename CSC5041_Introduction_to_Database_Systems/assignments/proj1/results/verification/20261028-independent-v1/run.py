from pathlib import Path
import subprocess,json,datetime,time,hashlib
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent

def run(tag,args,input=None,expect=0):
 t=datetime.datetime.now(datetime.timezone.utc).isoformat(); start=time.monotonic()
 p=subprocess.run(args,input=input,text=True,capture_output=True,cwd=ROOT)
 (OUT/(tag+'.stdout.txt')).write_text(p.stdout);(OUT/(tag+'.stderr.txt')).write_text(p.stderr)
 (OUT/(tag+'.json')).write_text(json.dumps(dict(time=t,argv=args,cwd=str(ROOT),exit=p.returncode,seconds=time.monotonic()-start,expected_exit=expect,input_sha256=hashlib.sha256(input.encode()).hexdigest() if input else None),indent=2))
 print(tag,p.returncode,flush=True)
 if p.returncode!=expect: raise RuntimeError(p.stderr)
 return p.stdout

def sql(db,tag,query):return run(tag,['psql','-X','-v','ON_ERROR_STOP=1','-d',db],query)
if __name__=='__main__':
 for suffix,precheck in [('plain',False),('checked',True)]:
  db='proj1_verify_20261028_'+suffix
  run('create-'+suffix,['createdb',db])
  run('import-'+suffix,['psql','-X','-v','ON_ERROR_STOP=1','--single-transaction','-d',db,'-f','data/import/MyDATASET.sql'])
  if precheck:run('checker-'+suffix,['psql','-X','-v','ON_ERROR_STOP=1','-d',db,'-f','project_release_to_students/check.sql'])
  run('load-'+suffix,['psql','-X','-v','ON_ERROR_STOP=1','--single-transaction','-d',db,'-f','src/proj1.sql'])
  if not precheck:run('checker-'+suffix,['psql','-X','-v','ON_ERROR_STOP=1','-d',db,'-f','project_release_to_students/check.sql'])
  q="SET statement_timeout='120s'; SELECT version(); SELECT * FROM check_all();\n"
  for n in range(1,11):
   q+=f"SELECT 'q{n}' as view, count(*) AS multiset_difference FROM ((SELECT * FROM q{n} EXCEPT ALL SELECT * FROM q{n}_expected) UNION ALL (SELECT * FROM q{n}_expected EXCEPT ALL SELECT * FROM q{n})) t;\n"
   q+=f'EXPLAIN (ANALYZE, TIMING ON, SUMMARY ON) SELECT * FROM q{n};\n'
  q+="SELECT c.relname,a.attname,format_type(a.atttypid,a.atttypmod) FROM pg_class c JOIN pg_attribute a ON a.attrelid=c.oid WHERE c.relname ~ '^q([1-9]|10)$' AND a.attnum>0 ORDER BY c.relname,a.attnum;"
  sql(db,'checks-'+suffix,q)
