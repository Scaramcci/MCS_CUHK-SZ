from run import run,OUT
run('edges-versions',['psql','-X','-v','ON_ERROR_STOP=1','-d','proj1_verify_20261028_plain','-f',str(OUT/'edges_versions.sql')])
