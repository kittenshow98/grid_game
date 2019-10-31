var amount = 2;
var set_id = 0;
function create_grid(amount,set_id) {
  function gridData() {
    var data = new Array();
    var xpos = 1; //starting xpos and ypos at 1 so the stroke will show when we make the grid below
    var ypos = 1;
    var total_width = 500;
    var total_height = 500;
    var click = 0;

    var width = total_width / amount;
    var height = total_height / amount;

    var id = -1;
    // iterate for rows
    for (var row = 0; row < amount; row++) {
      data.push(new Array());

      // iterate for cells/columns inside rows
      for (var column = 0; column < amount; column++) {
        id ++;
        data[row].push({
          x: xpos,
          y: ypos,
          width: width,
          height: height,
          click: click,
          id: id
        })
        // increment the x position. I.e. move it over by 50 (width variable)
        xpos += width;
      }
      // reset the x position after a row is complete
      xpos = 1;
      // increment the y position for the next row. Move it down 50 (height variable)
      ypos += height;
    }
    return data;
  }

  var gridData = gridData();
// I like to log the data to the console for quick debugging
  console.log(gridData);

  var random_num = d3.range(1).map(function() {
    return Math.random();
  });
  random_num = parseInt(random_num * 10000 % (amount**2));
  console.log("!!"+random_num);

  var grid = d3.select("#grid")
    .append("svg")
    .attr("width", "510px")
    .attr("height", "510px");

  var row = grid.selectAll(".row")
    .data(gridData)
    .enter().append("g")
    .attr("class", "row");

  var column = row.selectAll(".square")
    .data(function (d) {
      return d;
    })
    .enter().append("rect")
    .attr("class", "square")
    .attr("x", function (d) {return d.x;})
    .attr("y", function (d) {return d.y;})
    .attr("width", function (d) {return d.width;})
    .attr("height", function (d) {return d.height;})
    .style("fill", "#fff")
    .style("stroke", "#222")
    .on('click', function (d) {
      console.log(d.id);
      if(d.id == random_num && enable == 1) {
        d.click++;
        if (amount != 9){
          amount++;
        }
        d3.select("svg").remove();
        create_grid(amount, set_id);
      }
    });
}

create_grid(amount,set_id);
