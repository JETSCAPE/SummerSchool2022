#include "MyJEL.h"
#include "JetScapeLogger.h"
#include <string>
#include <iostream>

using namespace Jetscape;
using namespace std;

// Register the module with the base class
RegisterJetScapeModule<MyJEL> MyJEL::reg("CustomModuleMyJEL");

MyJEL::MyJEL()
{
  SetId("MyJEL");
  VERBOSE(8);
}

MyJEL::~MyJEL()
{
  VERBOSE(8);
}

void MyJEL::Init()
{
  JSINFO<<"Intialize Custom Jet Energy loss module ...";

  std::string s = GetXMLElementText({"Eloss", "CustomModuleMyJEL", "name"});
  JSINFO << s << " initializied ...";

}


void MyJEL::WriteTask(weak_ptr<JetScapeWriter> w)
{
  VERBOSE(8);  auto f = w.lock();
  if ( !f ) return;
  f->WriteComment("ElossModule Parton List: "+GetId());
  f->WriteComment("Energy loss to be implemented accordingly ...");
}

void MyJEL::DoEnergyLoss(double deltaT, double time, double Q2, vector<Parton>& pIn, vector<Parton>& pOut)
{
  
  JSINFO << "MyJEL::DoEnergyLoss is running! Success :)";
  //JSINFO << "pIn: ";
  //for (auto p : pIn) {
  //  JSINFO << p.E();
  //}
      
}
