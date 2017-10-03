$(document).ready(function() {
  (function () {
    $("#submit-task").click(function () {
      if (!Judicious.validate()) {
        return;
      }
      $('body').fadeOut(650);
      Judicious.postResult(
        Judicious.taskUUID,
        Judicious.result,
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
