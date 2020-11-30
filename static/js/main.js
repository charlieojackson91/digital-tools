function merge_words(){
	var out = "";
	var col1 = document.getElementById("merge1").value.split("\n");
	var col2 = document.getElementById("merge2").value.split("\n");
	for (i = 0; i < col1.length; i++){
		for(iter = 0; iter < col2.length; iter++){
			out += col1[i] + " " + col2[iter] + "\n";
			document.getElementById("merge-output").innerHTML = out; 			
			
		}
		
	}
	
}


function forecast(){
  var x = document.getElementById("numbers").value;
  var ctr = [0.18000, 0.09000, 0.07600, 0.06000, 0.05500, 0.05000, 0.03000, 0.02250, 0.01500, 0.01000, 0.00850, 0.00800, 0.00750, 0.00700, 0.00650, 0.00600, 0.00550, 0.00500, 0.0050,0.00450]
  var running = "";
  var first_slice = x.split('\n');
  for (var i = 0; i < first_slice.length; i++) {
    var second_slice = first_slice[i].split(';')
    if (second_slice[1] == 1) {
      var total = second_slice[0] * ctr[0];
      running += total.toString() + "\n";
    } if (second_slice[1] == 2) {
      var total = second_slice[0] * ctr[1];
      running += total.toString() + "\n";
    } if (second_slice[1] == 3) {
      var total = second_slice[0] * ctr[2];
      running += total.toString() + "\n";
    } if (second_slice[1] == 4) {
      var total = second_slice[0] * ctr[3];
      running += total.toString() + "\n";
    } if (second_slice[1] == 5) {
      var total = second_slice[0] * ctr[4];
      running += total.toString() + "\n";
    } if (second_slice[1] == 6) {
      var total = second_slice[0] * ctr[5];
      running += total.toString() + "\n";
    } if (second_slice[1] == 7) {
      var total = second_slice[0] * ctr[6];
      running += total.toString() + "\n";
    } if (second_slice[1] == 8) {
      var total = second_slice[0] * ctr[7];
      running += total.toString() + "\n";
    } if (second_slice[1] == 9) {
      var total = second_slice[0] * ctr[8];
      running += total.toString() + "\n";
    } if (second_slice[1] == 10) {
      var total = second_slice[0] * ctr[9];
      running += total.toString() + "\n";
    } if (second_slice[1] == 11) {
      var total = second_slice[0] * ctr[10];
      running += total.toString() + "\n";
    } if (second_slice[1] == 12) {
      var total = second_slice[0] * ctr[11];
      running += total.toString() + "\n";
    } if (second_slice[1] == 13) {
      var total = second_slice[0] * ctr[12];
      running += total.toString() + "\n";
    } if (second_slice[1] == 14) {
      var total = second_slice[0] * ctr[13];
      running += total.toString() + "\n";
    } if (second_slice[1] == 15) {
      var total = second_slice[0] * ctr[14];
      running += total.toString() + "\n";
    } if (second_slice[1] == 16) {
      var total = second_slice[0] * ctr[15];
      running += total.toString() + "\n";
    } if (second_slice[1] == 17) {
      var total = second_slice[0] * ctr[16];
      running += total.toString() + "\n";
    } if (second_slice[1] == 18) {
      var total = second_slice[0] * ctr[17];
      running += total.toString() + "\n";
    } if (second_slice[1] == 19) {
      var total = second_slice[0] * ctr[18];
      running += total.toString() + "\n";
    } if (second_slice[1] > 19) {
      var total = second_slice[0] * 0;
      running += total.toString() + "\n";
    } if (second_slice[1] < 1) {
      var total = second_slice[0] * 0;
      running += total.toString() + "\n";
    }
    document.getElementById('forecast').innerHTML = running;
  }
}


