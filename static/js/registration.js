$(function () {
    $("#submit-signing-button").prop("disabled", true);

    $("#id_privacy_and_cookie_policy_acceptance").on('change', function () {
        $("#submit-signing-button").prop("disabled", !$(this).is(":checked"));
    });
});