// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;
pragma experimental ABIEncoderV2;

contract SkillCertification {
    struct Certification {
        address user;
        string skill;
        string documentHash;
        string status;  // Pending, Verified, Rejected
        uint256 createdAt;  // Timestamp when certification was added
    }
    
    mapping(address => Certification[]) public certifications;
    
    event CertificationAdded(address indexed user, string skill, string documentHash);
    event CertificationVerified(address indexed user, string skill);
    event CertificationRejected(address indexed user, string skill);
    
    function addCertification(string memory skill, string memory documentHash) public {
        certifications[msg.sender].push(Certification(
            msg.sender, 
            skill, 
            documentHash, 
            "Pending", 
            block.timestamp
        ));
        emit CertificationAdded(msg.sender, skill, documentHash);
    }
    
    function verifyCertification(address user, uint index) public {
        require(index < certifications[user].length, "Invalid certification index");
        certifications[user][index].status = "Verified";
        emit CertificationVerified(user, certifications[user][index].skill);
    }
    
    function rejectCertification(address user, uint index) public {
        require(index < certifications[user].length, "Invalid certification index");
        certifications[user][index].status = "Rejected";
        emit CertificationRejected(user, certifications[user][index].skill);
    }
    
    function getCertifications(address _user) public view returns (Certification[] memory) {
        return certifications[_user];
    }
}