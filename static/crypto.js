function grab_keys(private_key, ekey) {
    var c = new BigInteger(window.atob(ekey), 10);
    var keywrap = new JSEncrypt();
    keywrap.setPrivateKey(private_key);

    var n = keywrap.key.n;
    var d = keywrap.key.d;
    var p = keywrap.key.p;
    var q = keywrap.key.q;
    var dmp1 = keywrap.key.dmp1;
    var dmq1 = keywrap.key.dmq1;

    if(p == null || q == null)
        return c.modPow(d, n);

        var cp = c.mod(p).modPow(dmp1, p);
        var cq = c.mod(q).modPow(dmq1, q);

        while(cp.compareTo(cq) < 0)
            cp = cp.add(p);

        return cp.subtract(cq).multiply(keywrap.key.coeff).mod(p).multiply(q).add(cq);
    }

function decrypt_msg(msg, priv, ekey, noncein) {
    var ret = grab_keys(priv, ekey);
    var key = parseHexString(ret.toString(16));

    var noncestr = window.atob(noncein);
    var nonceint = new BigInteger(noncestr, 10);
    var nonce = parseHexString(nonceint.toString(16));

    return decrypt_salsa_msg(key, nonce, msg);
}

function verify_msg(enc_msg, enc_ver_key, ver, priv) {
    var ver_key = grab_keys(priv, enc_ver_key).toString(16);
    var hmac = new jsSHA(enc_msg, "TEXT").getHMAC(ver_key, "TEXT", "SHA-256", "HEX");

    return hmac == ver;
}
