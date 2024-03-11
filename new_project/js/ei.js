const getRandomValues = require("get-random-values");

function s(e) {
    var t = null
      , r = 0
    t = getRandomValues(new Uint8Array(31));
    for (var i = [], o = 0; o < e; o++)
        i.push(a().toString(16));
    return i.join("");
    function a() {
        return t ? 15 & t[r++] : 16 * Math.random() | 0
    }
}
var b = getRandomValues(new Uint8Array(10));
console.table({"b": b});

var spanId = s(16);
var traceId = s(32);

// (window.NREUM || (NREUM = {})).loader_config = {
//     agentID: "1588758972",
//     accountID: "1273121",
//     trustKey: "2038175",
//     xpid: "VQQAUldRCRABUVRbAwAGUlcE",
//     licenseKey: "2f90a42388",
//     applicationID: "1559411435"
// };

var agentID = "1588758972", accountID = "1273121", trustKey = "2038175", xpid = "VQQAUldRCRABUVRbAwAGUlcE",  licenseKey = "2f90a42388", applicationID = "1559411435"

var c = Date.now();
// var spanId = "569614ea7d0579b8"
// var traceId = "c7c9724fdd52188a783973657507b490"

"00-569614ea7d0579b8-c7c9724fdd52188a783973657507b490-01"

"2038175@nr=0-1-1273121-1588758972-569614ea7d0579b8----1681353832701"

function generateTraceContextParentHeader(e, t) {
    return "00-" + t + "-" + e + "-01"
};



function generateTraceContextStateHeader(e, t, r, n, i) {
    return i + "@nr=0-1-" + r + "-" + n + "-" + e + "----" + t
};

var traceparent = generateTraceContextParentHeader(traceId, spanId);
var tracestate = generateTraceContextStateHeader(spanId, c, accountID, agentID, trustKey);

console.table({"traceparent": traceparent,
                "tracestate": tracestate});

function generateTraceHeader(e, t, r, n, i, o) {
    if (!("function" == typeof h._A?.btoa))
        return null;
    var a = {
        v: [0, 1],
        d: {
            ty: "Browser",
            ac: n,
            ap: i,
            id: e,
            tr: t,
            ti: r
        }
    };
    return o && n !== o && (a.d.tk = o),
    btoa((0, N.P)(a))
}