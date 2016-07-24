phoretic: phoretic.c param.h
	gcc $< -lm -O3 -LNO -march=corei7-avx -o $@

#Remove executable and data generated
.PHONY: clean
clean:
	rm -rf FieldData ParticleData phoretic
	rm *.dat cfield.mp4 particle.mp4 quiver.mp4

#Run simulation and generate raw data
.PHONY: dats
dats : particles.dat cfield.dat

%.dat: phoretic
	./phoretic
