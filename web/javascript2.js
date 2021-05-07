
var funbag = ['Welcome\x20back\x20admin!\x20Here\x20is\x20your\x20flag:\x0a', 'join', 'getElementById', 'charCodeAt', 'NzE6NzQ6Njc6Nzg6NDM6NTY6OTY6MjoxMDU6Nzo1MzoxMDU6NTA6NTY6OTg6NTE6OTg6ODM6NDg6OTc6NTU6NTQ6NTY6NjU6MTA1OjEwNDo1MDo4Mzo2MTo4OTo1Mjo2NToxMDE6NjU6NTQ6MTEzOjYyOjM=', 'inputEmail', 'length', 'inputPassword', '2718587a3f', 'value'];

(function (param1, param2) {
    ++param2;
    while (--param2) {
        param1.push(param1.shift());
        // param1['push'](param1['shift']());
    }
}(funbag, 150));

////////////////////////////////

const funbag = [
  /* 0 */ 'Welcome back admin! Here is your flag:\n',
  /* 1 */ 'join',
  /* 2 */ 'getElementById',
  /* 3 */ 'charCodeAt',
  /* 4 */ 'NzE6NzQ6Njc6Nzg6NDM6NTY6OTY6MjoxMDU6Nzo1MzoxMDU6NTA6NTY6OTg6NTE6OTg6ODM6NDg6OTc6NTU6NTQ6NTY6NjU6MTA1OjEwNDo1MDo4Mzo2MTo4OTo1Mjo2NToxMDE6NjU6NTQ6MTEzOjYyOjM=',
  /* 5 */ 'inputEmail',
  /* 6 */ 'length',
  /* 7 */ 'inputPassword',
  /* 8 */ '2718587a3f',
  /* 9 */ 'value'
]

var getFunbagOffset = function (offset) {
    offset = offset - 0; // convert to int
    return funbag[offset];
};
function fuzz(param1) {
    return param1 % 2 == 0 ? param1 + 3 : param1 - 1;
}
function keyValueAt(param1, param2) {
    var var2 = param2 % param1.length,
        var3 = parseInt(param1[var2]);
    return var3 && !isNaN(var3)
        ? var3
        : param1.charCodeAt(var2);
}
function encrypt(param1, param2) {
     var var1 = [];
     for (let i = 0; i < param2.length; i++) {
         var1.push(fuzz(param2.charCodeAt(i) ^ keyValueAt(param1, i)));
     }
     return btoa(var1.join(':'));
}

function login(_0x147be8) {
    var var1 = '2718587a3f',
        var2 = getFunbagOffset(4),
        var3 = document.getElementById("inputEmail"),
        var4 = document.getElementById("inputPassword"),
        var5 = var3.value,
        var6 = var4.value;
    return var5 === 'admin@local' && var6.length === 38 && var2 === encrypt(var1, var6)
        ? alert(var6)
        : alert('Bad\x20credentials!'),
        ![];
}





var respa2 = [
  "71", "74", "67", "78", "43", "56", "96", "2", "105", "7", "53", "105", "50", "56", "98", "51", "98", "83", "48", "97", "55", "54", "56", "65", "105", "104", "50", "83", "61", "89", "52", "65", "101", "65", "54", "113", "62", "3"
].map(x => +x);

fixKeyValueAt = (index) => {
    let var3 = parseInt("2718587a3f"[index]);
    return var3 && !isNaN(var3)
        ? var3
        : "2718587a3f".charCodeAt(index % ("2718587a3f".length));
};

unfuzz = a => a % 2 == 0 ? a + 1 : a - 3;

decrypt = (param2) => {
    var var1 = [];
    for (let i = 0; i < param2.length; i++) {
        var1.push(unfuzz(param2[i]) ^ keyValueAt("2718587a3f", i));
    }
    return var1;
}

decode = p => decrypt(p.map(x => parseInt(x))).map(x => x < 10 ? "" + x : String.fromCharCode(x));

result = p => decrypt(p.map(x => parseInt(x))).join(':');

var result = [ ];
var characters = [...new Array(126)].map((_, i) => i);
for (let i = 0; i < respa2.length; ++i) {
    for (let ch of characters) {
        if ((fuzz(ch ^ keyValueAt("2718587a3f", i))) == respa2[i]) {
            result.push(ch);
            break;
        }
    }
}
