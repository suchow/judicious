$(document).ready(function() {
  (function () {
    $("#submit-task").click(function () {
      var result;
      if (typeof Judicious.result === "function") {
        result = Judicious.result();
      } else {
        result = Judicious.result;
      }
      if (!Judicious.validate(result)) {
        return;
      }
      $('body').fadeOut(650);
      Judicious.postResult(
        Judicious.taskUUID,
        result,
        function () {
          if (Judicious.turkSubmitTo !== '') {
            $("#mturk_form").submit();
          } else {
            location.reload();
          }
        }
      );
    });
    $("#skip-task").click(function () {
      location.reload();
    });
  })();
});
