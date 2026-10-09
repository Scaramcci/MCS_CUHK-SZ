from itertools import product
H=lambda x:int(x>=0)
for x1,x2 in product([0,1],repeat=2):
 z1=H(x1+x2-.5);z2=H(x1+x2-1.5);y=H(z1-2*z2-.5)
 assert y==(x1!=x2)
 print(x1,x2,z1,z2,y)
# New XOR impossibility argument independently checked algebraically:
# w1+b >=0 and w2+b >=0 imply w1+w2+2b >=0.
# Subtract b: w1+w2+b >= -b. Since b<0, -b>0,
# contradicting the required negative score at (1,1).
# New chain-rule expression interpreted as Jacobian multiplication:
# gradient L wrt first-layer weights = dL/dy * dy/dz * dz/dw1.
# For scalar toy composition y=z*z,z=w*x,L=.5*(y-t)**2:
w,x,t=0.7,1.3,0.4
f=lambda w:.5*((w*x)**2-t)**2
z=w*x;y=z*z
chain=(y-t)*(2*z)*x
eps=1e-6;finite=(f(w+eps)-f(w-eps))/(2*eps)
assert abs(chain-finite)<1e-7
print('scalar chain rule',chain,'finite-difference independent check',finite)
print('XOR proof: correct by algebra; threshold forward network all four inputs passed.')
