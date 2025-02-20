#ifndef FUNCTIONS_LOWPU_H
#define FUNCTIONS_LOWPU_H

#define MUON_MASS 0.1056583
#define ELEC_MASS 0.000511
#include "TClonesArray.h"


float CalculateTransverseMass(float particle_pt, float particle_phi, float met, float metPhi) {
    // Extract muon transverse momentum and phi

    // Calculate delta phi
    float deltaPhi = std::abs(particle_phi - metPhi);
    if (deltaPhi > M_PI) {
        deltaPhi = 2 * M_PI - deltaPhi; // Ensure deltaPhi is in [0, pi]
    }

    // Calculate transverse mass
    float mt = std::sqrt(2 * particle_pt * met * (1 - std::cos(deltaPhi)));
    return mt;
}



TLorentzVector GetHighestPT_particle(const ROOT::VecOps::RVec<TLorentzVector>& particles) {
    if (particles.empty()) {
        throw std::invalid_argument("Particle vector is empty.");
    }

    // Initialize the highest-pT muon as the first one
    TLorentzVector highestPT_particle = particles[0];

    // Iterate through the muons to find the one with the highest pT
    for (const auto& particle : particles) {
        if (particle.Pt() > highestPT_particle.Pt()) {
            highestPT_particle = particle;
        }
    }

    return highestPT_particle;
}




ROOT::VecOps::RVec<TLorentzVector> Get_resonance_Pair(ROOT::VecOps::RVec<TLorentzVector> particles,float targetMass) {

    double closestDiff = std::numeric_limits<double>::max();
    ROOT::VecOps::RVec<TLorentzVector> result(4);
    std::vector<size_t> bestPairIndices(2, 0); // To track indices of the best pair

    // Loop over all unique pairs of TLorentzVector objects
    for (size_t i = 0; i < particles.size(); ++i) {
        for (size_t j = i + 1; j < particles.size(); ++j) {
            // Calculate the invariant mass of the pair
            double invariantMass = (particles[i] + particles[j]).M();

            // Check if this pair is closer to the target mass
            double diff = std::abs(invariantMass - targetMass);
            if (diff < closestDiff) {
                closestDiff = diff;
                bestPairIndices = {i, j};
            }
        }
    }

    result[0] = particles[bestPairIndices[0]];
    result[1] = particles[bestPairIndices[1]];

    ROOT::VecOps::RVec<TLorentzVector> remainingParticles;
    for (size_t i = 0; i < particles.size(); ++i) {
        if (i != bestPairIndices[0] && i != bestPairIndices[1]) {
            remainingParticles.push_back(particles[i]);
        }
    }


    std::sort(remainingParticles.begin(), remainingParticles.end(),
              [](const TLorentzVector& a, const TLorentzVector& b) {
                  return a.Pt() > b.Pt();
              });

    if (!remainingParticles.empty()) {
        result[2] = remainingParticles[0];
            }
    if (remainingParticles.size() > 1) {
        result[3] = remainingParticles[1];
    }

    return result;
   

}




ROOT::VecOps::RVec<TLorentzVector>  makeLorentzVectors(ROOT::VecOps::RVec<float>  jets_pt, ROOT::VecOps::RVec<float>  jets_eta, ROOT::VecOps::RVec<float>  jets_phi, ROOT::VecOps::RVec<float>  jets_m){
ROOT::VecOps::RVec<TLorentzVector> result;
    for(int i=0; i<jets_pt.size(); i++) {
         TLorentzVector tlv;
         tlv.SetPtEtaPhiM(jets_pt[i], jets_eta[i], jets_phi[i], jets_m[i]);
        result.push_back(tlv);
    }
    return result;


   }


double deltaPhi(float phi1, float phi2) {
    double result = phi1 - phi2;
    while (result > M_PI) result -= 2.0*M_PI;
    while (result <= -1.0*M_PI) result += 2.0*M_PI;
    return result;
}

double delR(const ROOT::Math::PtEtaPhiMVector particle1,const ROOT::Math::PtEtaPhiMVector particle2) {
    double deta = particle1.Eta()-particle2.Eta();
    double dphi = particle1.Phi()-particle2.Phi();
    return sqrt(deta*deta + dphi*dphi);
}


ROOT::Math::PtEtaPhiMVector sumP4(ROOT::VecOps::RVec<double> pt, ROOT::VecOps::RVec<double> eta, ROOT::VecOps::RVec<double> phi, ROOT::VecOps::RVec<double> m) {

    ROOT::Math::PtEtaPhiMVector ret(0, 0, 0, 0);
	for(unsigned int i = 0; i < pt.size(); ++i) {
        
        ROOT::Math::PtEtaPhiMVector v(pt[i], eta[i], phi[i], m[i]);
        ret += v;
    }
  
    return ret;
}



#endif
