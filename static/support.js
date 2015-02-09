function parseHexString(str) {
    a = [];

    for (var i = 0; i < str.length; i += 2) {
        a.push(parseInt(str.substr(i, 2), 16));
    }
    return a;
}
function b64tohex(s) {
    var ret = ""
    var i;
    var k = 0; // b64 state, 0-3
    var slop;
    for(i = 0; i < s.length; ++i) {
        if(s.charAt(i) == b64pad) break;
        v = b64map.indexOf(s.charAt(i));
        if(v < 0) continue;
        if(k == 0) {
            ret += int2char(v >> 2);
            slop = v & 3;
            k = 1;
        }
        else if(k == 1) {
            ret += int2char((slop << 2) | (v >> 4));
            slop = v & 0xf;
            k = 2;
        }
        else if(k == 2) {
            ret += int2char(slop);
            ret += int2char(v >> 2);
            slop = v & 3;
            k = 3;
        }
        else {
            ret += int2char((slop << 2) | (v >> 4));
            ret += int2char(v & 0xf);
            k = 0;
        }
    }
    if(k == 1)
        ret += int2char(slop << 2);
    return ret;
}

var BI_RM = "0123456789abcdefghijklmnopqrstuvwxyz";
var BI_RC = new Array();
var rr,vv;
rr = "0".charCodeAt(0);
for(vv = 0; vv <= 9; ++vv) BI_RC[rr++] = vv;
rr = "a".charCodeAt(0);
for(vv = 10; vv < 36; ++vv) BI_RC[rr++] = vv;
rr = "A".charCodeAt(0);
for(vv = 10; vv < 36; ++vv) BI_RC[rr++] = vv;

function int2char(n) { return BI_RM.charAt(n); }

var b64map="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var b64pad="=";

var ZERO   = '0'.charCodeAt(0)
var PLUS   = '+'.charCodeAt(0)
var SLASH  = '/'.charCodeAt(0)
var NUMBER = '0'.charCodeAt(0)
var LOWER  = 'a'.charCodeAt(0)
var UPPER  = 'A'.charCodeAt(0)

function decode (elt) {
    var code = elt.charCodeAt(0)
    if (code === PLUS)
        return 62 // '+'
    if (code === SLASH)
        return 63 // '/'
    if (code < NUMBER)
        return -1 //no match
    if (code < NUMBER + 10)
        return code - NUMBER + 26 + 26
    if (code < UPPER + 26)
        return code - UPPER
    if (code < LOWER + 26)
        return code - LOWER + 26
}

function b64ToByteArray (b64) {
    var i, j, l, tmp, placeHolders, arr

    if (b64.length % 4 > 0) {
        throw new Error('Invalid string. Length must be a multiple of 4')
    }

    // the number of equal signs (place holders)
    // if there are two placeholders, than the two characters before it
    // represent one byte
    // if there is only one, then the three characters before it represent 2 bytes
    // this is just a cheap hack to not do indexOf twice
    var len = b64.length
    placeHolders = '=' === b64.charAt(len - 2) ? 2 : '=' === b64.charAt(len - 1) ? 1 : 0

    // base64 is 4/3 + up to two characters of the original data
    arr = new Array(b64.length * 3 / 4 - placeHolders)

    // if there are placeholders, only get up to the last complete 4 chars
    l = placeHolders > 0 ? b64.length - 4 : b64.length

    var L = 0

    function push (v) {
        arr[L++] = v
    }

    for (i = 0, j = 0; i < l; i += 4, j += 3) {
        tmp = (decode(b64.charAt(i)) << 18) | (decode(b64.charAt(i + 1)) << 12) | (decode(b64.charAt(i + 2)) << 6) | decode(b64.charAt(i + 3))
        push((tmp & 0xFF0000) >> 16)
        push((tmp & 0xFF00) >> 8)
        push(tmp & 0xFF)
    }

    if (placeHolders === 2) {
        tmp = (decode(b64.charAt(i)) << 2) | (decode(b64.charAt(i + 1)) >> 4)
        push(tmp & 0xFF)
    } else if (placeHolders === 1) {
        tmp = (decode(b64.charAt(i)) << 10) | (decode(b64.charAt(i + 1)) << 4) | (decode(b64.charAt(i + 2)) >> 2)
        push((tmp >> 8) & 0xFF)
        push(tmp & 0xFF)
    }

    return arr;
}
