import localization as lx

P=lx.Project(mode='Earth1',solver='CCA')
# print str(P)

P.add_anchor('1',(18.530143, 73.854764))
P.add_anchor('2',(18.530835, 73.856097))
P.add_anchor('3',(18.530637, 73.857547))

t,label=P.add_target()


print str(t),'-----', str(label)

t.add_measure('1', 216)
t.add_measure('2', 160)
t.add_measure('3', 173)

P.solve()
# print str(B)

B = t.loc
print str(B)
# print 'location: ', str(ecef2llh((B.x, B.y, B.z)))