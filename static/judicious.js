var Judicious = (function () {
  result = {
    foo: 'bar',
  };
  validate = function () { return true; };
  var postResult = function (uuid, result, callback) {
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
