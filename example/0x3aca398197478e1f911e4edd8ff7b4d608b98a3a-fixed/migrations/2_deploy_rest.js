const EncryptedToken =  artifacts.require("EncryptedToken");
const owned = artifacts.require("owned");

module.exports = function (deployer) {
    deployer.deploy(owned);
    deployer.deploy(EncryptedToken);
  };