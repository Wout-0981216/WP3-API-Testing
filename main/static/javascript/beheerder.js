
function updateOpenRequestsCount() {
            $.ajax({
                url: '/get_aanvragen',
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    $('#investigationCount1').text(data.aanvragen);
                },
                error: function (error) {
                    console.log('Fout bij het ophalen van openstaande aanvragen:', error);
                }
            });
        }

        $(document).ready(function () {
            updateOpenRequestsCount();
        });

        setInterval(function () {
            updateOpenRequestsCount();
        }, 10000);