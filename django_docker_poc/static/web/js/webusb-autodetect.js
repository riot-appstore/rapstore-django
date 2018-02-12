/*
 * Copyright (C) 2017-2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

filterRules = [
    //all values are mandatory, even if they are null
    //vendorId and productId are used for WebUSB API, boardInternalName is ignored by it
    {vendorId: 0x0d28, productId: 0x0204, boardInternalName: "pba-d-01-kw2x"},              //Phytec phyWAVE-KW22
    {vendorId: 0x0483, productId: 0x374b, boardInternalName: "nucleo-f103"},                //Nucleo-F103
    {vendorId: 0x0483, productId: 0x374b, boardInternalName: "nucleo-f334"},                //Nucleo-F334
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f091"},                //Nucleo-F091
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f072"},                //Nucleo-F072
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f070"},                //Nucleo-F070
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo-f030"},                //Nucleo-F030
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo32-f303"},              //Nucleo32-F303
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo32-f042"},              //Nucleo32-F042
    {vendorId: 0x0483, productId: null  , boardInternalName: "nucleo32-f031"},              //Nucleo32-F031
    {vendorId: 0x2047, productId: null  , boardInternalName: "MSP430 (family)"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "ATmega (family)"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "MIPS (family)"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "Nucleo family"},
    {vendorId: 0x0483, productId: 0x3748, boardInternalName: "Airfy Beacon"},
    {vendorId: 0x2a03, productId: 0x003d, boardInternalName: "Arduino Due (usb2serial)"},
    {vendorId: 0x2a03, productId: 0x003e, boardInternalName: "Arduino Due"},
    {vendorId: 0x03eb, productId: 0x6121, boardInternalName: "Arduino Zero"},
    {vendorId: 0x0403, productId: null  , boardInternalName: "CC2650STK"},
    {vendorId: 0x0403, productId: 0xa6d1, boardInternalName: "CC2538DK"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "LimiFrog-v1"},
    {vendorId: 0x0d28, productId: 0x0204, boardInternalName: "mbed_lpc1768"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "micro:bit"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "MSB-IoT"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "NZ32-SC151"},
    {vendorId: 0x0451, productId: null  , boardInternalName: "OpenMote"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "PCA1000x (nRF51822 Development Kit)"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "RFduino"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "SAMD21-xpro"},
    {vendorId: 0x0d28, productId: null  , boardInternalName: "Seeeduino Arch-Pro"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "SODAQ Autonomo"},
    {vendorId: 0x1d50, productId: 0x607f, boardInternalName: "Spark Core"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "SparkFun SAMD21 Mini"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "STM32F0discovery"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "STM32F3discovery"},
    {vendorId: 0x0483, productId: null  , boardInternalName: "STM32F4discovery"},
    {vendorId: 0x1915, productId: null  , boardInternalName: "yunjia-nrf51822"},
    {vendorId: 0x03eb, productId: 0x0042, boardInternalName: "Arduino Mega2560"},
    {vendorId: 0x03eb, productId: 0x0043, boardInternalName: "Arduino Uno"},
    {vendorId: 0x03eb, productId: null  , boardInternalName: "Arduino Duemilanove"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "MSB-430H"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "TelosB"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "WSN430"},
    {vendorId: 0x2047, productId: null  , boardInternalName: "eZ430-Chronos"},
    {vendorId: 0x04d8, productId: 0x00e0, boardInternalName: "PIC32-WiFire"},
    {vendorId: 0x042b, productId: null  , boardInternalName: "Intel Galileo"},
    {vendorId: 0x8086, productId: null  , boardInternalName: "Intel Galileo"},
    {vendorId: 0x8087, productId: null  , boardInternalName: "Intel Galileo"},
    {vendorId: null  , productId: null  , boardInternalName: "HikoB Fox"},
    {vendorId: null  , productId: null  , boardInternalName: "IoT LAB M3"},
    {vendorId: null  , productId: null  , boardInternalName: "MSBA2"},
    {vendorId: null  , productId: null  , boardInternalName: "Mulle"},
    {vendorId: null  , productId: null  , boardInternalName: "UDOO"},
    {vendorId: null  , productId: null  , boardInternalName: "Zolertia remote"},
    {vendorId: null  , productId: null  , boardInternalName: "Zolertia Z1"},
]


async function autodetect(selectorID) {

/*
unless otherwise specified, following vendorid and productid entries are coming from:
    http://www.linux-usb.org/usb.ids
*/

    navigator.usb.requestDevice({filters: filterRules})
    .then(selectedDevice => {
            device = selectedDevice;
            return device;
     })
    .then(() => {

        selectedRule = null;
        //first rule which fits is taken by this algorithm
        for (var i = 0; i < filterRules.length; i++) {
            rule = filterRules[i];

            if (rule.vendorId != null && rule.productId != null) {
                if (rule.vendorId == device.vendorId && rule.productId == device.productId) {
                    selectedRule = rule;
                    break;
                }
            }
            else if (rule.vendorId != null) {
                if (rule.vendorId == device.vendorId) {
                    selectedRule = rule;
                    break;
                }
            }
        }

        if (selectedRule == null) {
            alert("Sorry, your board could not be recognized :(");
        }
        else {
            console.log(selectedRule.boardInternalName);
            document.getElementById(selectorID).value = selectedRule.boardInternalName;
        }

        return device;
    })
    .catch(error => {
        console.log(error);
    });

}
