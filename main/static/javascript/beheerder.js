
function updateInschrijvingen() {
            $.ajax({
                url: '/get_evd',
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    $('#investigationCount3').text(data.evd);
                },
                error: function (error) {
                    console.log('Fout bij het ophalen van openstaande aanvragen:', error);
                }
            });
        }

function updateOnderzoeken() {
            $.ajax({
                url: '/get_onderzoeken',
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    $('#investigationCount2').text(data.onderzoeken);
                },
                error: function (error) {
                    console.log('Fout bij het ophalen van openstaande aanvragen:', error);
                }
            });
        }

function updateRegistraties() {
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
            updateRegistraties();
            updateOnderzoeken();
            updateInschrijvingen();

        });

        setInterval(function () {
            updateRegistraties();
            updateOnderzoeken();
            updateInschrijvingen();
        }, 10000);