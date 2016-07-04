/* Compile line on LINUX
cc  phoretic.c -lm -O3 -LNO -o phoretic
*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*useful constants*/
#define Pi 3.141592653589793
#define TwoPi 6.283185307179586
#define sqr2 1.4142136
#define FourPi 12.566370614359173
#define Inv12Pi 0.026525823848649223
#define Inv4Pi 0.079577471545947668
#define Inv8Pi 0.039788735772973834

/*program parameters*/
#include "param.h"

/*global variables*/

/*particles */

double particle_x[nparticles]; // x position of particles
double particle_y[nparticles]; // y position of particles 
double particle_dir[nparticles]; // direction of particles, this is an angle

double Dr=0.2; // rotational diffusion
double v0=2.0; // 2.5 // //1.0 // 0.5 // particle velocity, constant and same for all
double dx=1.0; // spatial step dx
double dxs; // scaled spatial step dx

double k0=0.0;// 3.0 // 5.0 // 0.5; //production rate // 0.02
double kd=0.01; // 0.001 // 0.1 decay rate // 0.001
double Dc=0.1; // 0.1 // 1.0 diffusion coefficient  // 0.001

double c_coup = -1.0; // -0.1 // -1.0 chemotactic coefficient: positive is chemoattractive

double ka = 5.0; // 10.0 asymmetry in production
double shift = -1.0; // -1.0 shift between centre and asymmetric production

/*PDE variables*/

double c[Lsx][Lsy],c_new[Lsx][Lsy];

FILE *output;
FILE *output2;

/*parameters for reaction-diffusion equation goes here */

/*function declarations*/

void reactiondiffusion(void); // this solves reaction-diffusion

void streamfile(int step);

int main(int argc, char** argv)
{
  int i,j,k,n,disx,disy,disxup,disxdwn,disyup,disydwn;
  double phase,browniannoise,forcing;

  dxs=dx/(double)(scaling);

  /*initialize particles here*/

  srand48(1231);

  for(n=0;n<nparticles;n++){
    phase= 2.0*Pi*(0.5-drand48());
    particle_dir[n] = phase;
    particle_x[n] = ((double)(Lx))*drand48();
    particle_y[n] = ((double)(Ly))*drand48();
  }
  
  /*initialize chemical field*/
    for (i=0;i<Lx;i++){
    for (j=0;j<Ly;j++){
      c[i][j]=0.1*drand48();
      c_new[i][j]=c[i][j];
    }
  }
  
  /*main for loop for dynamics is below*/

  for(i = 0; i < number_step; i++){ 

    /*move particles */

    for(n = 0; n < nparticles; n++){
		
	  /* Remember: scaling > 1, and round() returns an integer. 
	   * So disx and disy are the chemical field lattice coordinates closest to the particle */
      disx = round(particle_x[n]*scaling); //-1 because c counts array positions from 0 to Lx-1
      disy = round(particle_y[n]*scaling);      
      if(disx<0) disx=Lsx+disx; if(disx>Lsx-1) disx=disx-Lsx;
      if(disy<0) disy=Lsy+disy; if(disy>Lsy-1) disy=disy-Lsy;
      disxup = disx+1;
      if(disx==Lsx-1) disxup=0;
      disxdwn=disx-1;
      if(disx==0) disxdwn=Lsx-1;
      disyup=disy+1;
      if(disy==Lsy-1) disyup=0;
      disydwn=disy-1;
      if(disy==0) disydwn=Lsx-1;
	  
	  /* dc/dx and dc/dy, needed for computing coupling with chemical field */
      double dxc=(c[disxup][disy]-c[disxdwn][disy])/(2.0*dxs);
      double dyc=(c[disx][disyup]-c[disx][disydwn])/(2.0*dxs);
      
      browniannoise=sqrt(2.0*Dr*dt)*sqrt(3.0)*(1.0-2.0*drand48());
      forcing = browniannoise+dt*c_coup*(cos(particle_dir[n])*dyc - sin(particle_dir[n])*dxc);
      particle_dir[n] += forcing;
      particle_x[n] += v0*cos(particle_dir[n])*dt;
      particle_y[n] += v0*sin(particle_dir[n])*dt;
      
      /*take care of periodic boundary conditions now */
      if(particle_x[n]>Lx) particle_x[n] -= Lx;
      if(particle_x[n]<0) particle_x[n] += Lx;
      if(particle_y[n]>Ly) particle_y[n] -= Ly;
      if(particle_y[n]<0) particle_y[n] += Ly;

    }

    /* evolve chemical field */

    reactiondiffusion();

    /*output every quantum steps */

    if(i%quantum == 0){
      streamfile(i);
      printf("%d\n",i);
    }

  }

}

void streamfile(int step)
{
  int i,j,n;

  if((output = fopen("particles.dat","a"))==NULL)
    {
      printf("I cannot open output file\n");
      exit(0);
    }

  for(n=0; n<nparticles; n++) {
    
    fprintf(output, "%d %16.8f %16.8f %16.8f \n",
	    step,particle_x[n],particle_y[n],particle_dir[n]);
  }
  
  fclose(output);

   if((output2 = fopen("cfield.dat","a"))==NULL)
    {
      printf("I cannot open output file\n");
      exit(0);
    }

  for(i=0; i<Lsx; i++){
    for(j=0; j<Lsy; j++){
    
      fprintf(output2, "%d %d %16.8f %16.8f\n",i,j,c[i][j],c_new[i][j]);
    }
  }
  fclose(output2);
  

}

void reactiondiffusion(void)
{
  int i,j,n,iup,idwn,jup,jdwn,kup,kdwn;
  double dcdx,dcdy,d2cdxdx,d2cdydy;
  double laplacian[Lx][Ly];
  int prodx,prody,prodax,proday;

  //do chemical production here
  for(n=0; n<nparticles; n++){
    	prodx=round(particle_x[n]*scaling); //-1 because c counts array positions from 0 to Lx-1
	prody=round(particle_y[n]*scaling);
	//	printf("%d %d %d\n",n,prodx,prody);
	if(prodx<0) prodx=Lsx+prodx;
	if(prody<0) prody=Lsy+prody;
	if(prodx>Lsx-1) prodx=-Lsx+prodx;
	if(prody>Lsy-1) prody=-Lsy+prody;
	/*if(prodx<0 || prodx>Lx-1) printf("ahi!\n");
	  if(prody<0 || prody>Ly-1) printf("ahi!!\n");*/
	c_new[prodx][prody] = c[prodx][prody]+dt*k0/(dxs*dxs); // symmetric production
	prodax=round((particle_x[n]+shift*cos(particle_dir[n]))*scaling); 
	proday=round((particle_y[n]+shift*sin(particle_dir[n]))*scaling); 
	if(prodax<0) prodax=Lsx+prodax;
	if(proday<0) proday=Lsy+proday;
	if(prodax>Lsx-1) prodax=-Lsx+prodax;
	if(proday>Lsy-1) proday=-Lsy+proday;
	c_new[prodax][proday] = c_new[prodax][proday]+dt*ka/(dxs*dxs); // asymmetric production
  }

  for(i=0;i<Lsx;i++){
    if (i==Lsx-1) iup=0; else iup=i+1;
    if (i==0) idwn=Lsx-1; else idwn=i-1;
    for (j=0; j<Lsy; j++) {
      if (j==Lsy-1) jup=0; else jup=j+1;
      if (j==0) jdwn=Lsy-1; else jdwn=j-1;
	
      //finite differences for laplacian for c goes here
      d2cdxdx=(c[iup][j]+c[idwn][j]-2.0*c[i][j])/(dxs*dxs);
      d2cdydy=(c[i][jup]+c[i][jdwn]-2.0*c[i][j])/(dxs*dxs);

      //update chemical concentration field here
      c_new[i][j]=c_new[i][j]+dt*Dc*(d2cdxdx+d2cdydy)-dt*kd*c[i][j];
    }
  }
  
  for (i=0;i<Lsx;i++){
    for (j=0;j<Lsy;j++){
      c[i][j]=c_new[i][j];
      c_new[i][j]=c[i][j];
    }
  }

}
