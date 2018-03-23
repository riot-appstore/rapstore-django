/*
 * Copyright (C) 2017-2018 Hendrik van Essen and FU Berlin
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
*/

function messageExtension(givenAction, givenMessage="") {

    window.postMessage({
        action: givenAction,
        message: givenMessage
    },
    "*");
}
