var Judicious = (function () {
  result = {
    foo: 'bar',
  };
  validate = function () { return true; };
  var postResult = function (uuid, result, callback) {
    if (typeof result === "function") {
      result = result();
    }
    console.log("Submitting result");
    console.log(result);
    $.ajax({
      url: '/tasks/' + uuid,
      type: 'PATCH',
      dataType: 'JSON',
      complete: function (data) {
        callback();
      },
      data: {'result': JSON.stringify(result)},
    });
  };
  return {
    postResult: postResult,
    result: result,
    validate: validate,
  };
})();
