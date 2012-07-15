var exit = new Bitcoin.ExitNode("217.197.81.123", 3125, /* SSL= */ false);
exit.connect(function () {
  exit.on('blockAdd', function (data) {
    console.log('Block', data);
  });
  exit.listen(['14HhYVs1hWhHa74wSsiwhzRmiXfTuyzQg5']);
});
