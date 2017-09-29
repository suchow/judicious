$(document).ready(function() {
  (function () {
    $("#submit-task").click(function () {
      Judicious.postResult(
        Judicious.taskUUID,
        Judicious.result,
        function () {
          location.reload();
        }
      );
    });
    $("#skip-task").click(function () {
      location.reload();
    });
  })();
});
