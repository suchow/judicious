$(function () {
    $("#race").bsMultiSelect({
        useCss: true,
    });

    $.validator.addMethod(
        "regex",
        function (value, element, regexp) {
            return this.optional(element) || regexp.test(value);
        },
        "Please check your input."
    );

    $.validator.addMethod(
        "selectValidEntry",
        function (value, element, arg) {
            return value !== "NA" && value !== "";
        },
        "Please select a valid answer from the dropdown list."
    );

    $.validator.addMethod("needsSelection", function (value, element) {
        const count = $(element).find("option:selected").length;
        return count > 0;
    });

    $("form[name='debriefingForm']").validate({
        rules: {
            whatTested: {
                required: true,
                minlength: 15,
            },
            strategies: {
                required: true,
                minlength: 15,
            },
            perceivedPerformance: {
                selectValidEntry: true,
            },
            interruption: {
                selectValidEntry: true,
            },
            issues: {
                required: true,
                minlength: 2,
            },
            comments: {
                required: false,
            },
            workerId: {
                required: true,
                minlength: 6,
                // ! XXX regex for worker ID?
            },
            age: {
                required: true,
                range: [18, 120],
            },
            gender: {
                selectValidEntry: true,
            },
            race: {
                needsSelection: true,
            },
            raceText: {
                required: false,
            },
        },

        messages: {
            age: {
                required: "Please enter your age.",
                min: "Please enter a valid adult age.",
                max: "Please enter a valid adult age.",
            },
            race: {
                needsSelection: "Please select at least one race.",
            },
        },

        ignore: ':hidden:not("#race")', // necessary due to bsMultiSelect

        highlight: function (element, errorClass, validClass) {
            $(element).addClass("is-invalid");
        },

        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass("is-invalid");
        },
    });
});
