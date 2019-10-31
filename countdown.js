// var formatTime = d3.timeFormat("Time Lef: %X"),
//     countdown = d3.select("#countdown");
//     today = d3.timeDay(new Date);
//     console.log(today)
// // 60s
// var deadline = d3.timeSecond.offset(60, 1);
// deadline.setSeconds(60);
//
// (function tick() {
//   var now = new Date;
//   countdown.text(formatTime(new Date(+deadline - d3.timeSecond(now))));
//   setTimeout(tick, 1000 - now % 1000);
// })();
function countdown() {
  var CD = d3.select("body")
    .append("div")
    .attr("id", "countdown")
    .style("opacity", 1);
  var countdown = d3.select("#countdown");
  var t = d3.timer(function (elapsed) {
    console.log((60 - parseInt(elapsed / 1000)).toString());
    var text = (60 - parseInt(elapsed / 1000)).toString();
    countdown.text("TIME LEFT: " + text);
  });

  d3.timeout(function () {
    t.stop();
    enable = 0;
    amount = 2;
    d3.select("svg").remove();
    create_grid(amount, set_id);
    alert("Time is up!");
    d3.select("#countdown").remove();
  }, 3000);
}
