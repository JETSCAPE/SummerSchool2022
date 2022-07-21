#ifndef MYJEL_H
#define MYJEL_H

#include "JetEnergyLossModule.h"

using namespace Jetscape;

class MyJEL : public JetEnergyLossModule<MyJEL>
{  
 public:
  
  MyJEL();
  virtual ~MyJEL();

  void Init();
  void DoEnergyLoss(double deltaT,double time, double Q2,
                    vector<Parton>& pIn, vector<Parton>& pOut);
  void WriteTask(weak_ptr<JetScapeWriter> w);

 private:
  // Allows the registration of the module so that it is available
  // to be used by the Jetscape framework.
  static RegisterJetScapeModule<MyJEL> reg;
  
};

#endif // MyJEL

