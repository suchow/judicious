var Judicious = (function () {
  result = {
    foo: 'bar',
  };
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
      success: function (data) {
        callback();
      },
      data: {'result': JSON.stringify(result)},
    });
  };
  return {
    result: result,
    postResult: postResult,
  };
})();
