const ShiftCashIco =  artifacts.require("ShiftCashIco");
const ShiftCashToken = artifacts.require("ShiftCashToken");

module.exports = function (deployer) {
    deployer.deploy(ShiftCashToken,'0x56a7214f81c527fea3b904130c4c549d550dfafd').then(function() {
        return deployer.deploy(ShiftCashIco, "0x293dd7b38eec74bf4e06bd5cd948aeee058f059b", ShiftCashToken.address);
    })
  };