var lastResponse = {
  beschikbaar: null,
  goedgekeurd: null,
  afgekeurde: null,
  afwachting: null,
};
var interval;
var INTERVAL_TIME = 5000;
var DOMINE_NAME = "localhost";
const getResearches = (type = "beschikbaar") => {
  $.ajax({
    url: `http://${DOMINE_NAME}:5000/ervaringsdeskundige/haal_onderzoek/${type}`,
    method: "GET",
  })
    .then((jsonResponse) => {
      if (jsonResponse.length > 0) {
     
        if (
          JSON.stringify(jsonResponse) !== JSON.stringify(lastResponse[type])
        ) {
          lastResponse[type] = jsonResponse;
          $(`#aantal-${type}-onderzoeken`).text(lastResponse[type].length);
          let listItems = "";
          lastResponse[type].forEach((element, index) => {
            let typeButton =
              type == "beschikbaar"
                ? `<button  onclick='deelname(event)'
                          id=onderzoek-id-${element.id}
                          type="button" class="btn btn-primary">Inschrijven</button>
                         `
                : `<button  onclick='uitschrijven(event)'
                          id=onderzoek-id-${element.id}
                          type="button" class="btn btn-danger">Uitschrijven</button>
                         `;

            listItems += `<li class='list-element' id='list-element-${
              element.id
            }'>
                          <span><i> ${index + 1} <i/> ${element.titel} </span>
                          <div>
                              <p>${element.beschrijving}</p>
                              <p><b>Beschikbaar van:</b> ${element.datum_vanaf} <b>tot:</b> ${element.datum_tot}</p>
                              <p><b>Onderzoekstype: </b>${element.type_onderzoek}</p>
                              <p><b>Locatie: </b>${element.locatie}</p>
                              <p><b>Leeftijds doelgroep: </b>${element.doelgroep_leeftijd_van}-${element.doelgroep_leeftijd_tot}</p>
                              <p><b>Beperking doelgroep: </b>${element.doelgroep_beperking}</p>
                              <p><b>Onderzoek van: </b>${element.organisatie_id}</p>
                              <p><b>Met beloning: </b>${element.met_beloning}</p>
                              <p><b>Beloning(indien van toepassing): </b>${element.beloning}</p>
                              <p><b>Status: </b>${element.inschrijving_ervaringsdeskundige_onderzoek_status}</p>

                          </div>
                          ${typeButton}
                          </li>`;
          });
          $(`#list-${type}`).html(listItems);
        }
      } else {
        $(`#list-${type}`).html(`<li>No Research found </li>`);
      }
    })
    .catch((error) => {});
};

function uitschrijven() {
  const resultConfirm = confirm("Bent u zeker! ");
  if (event && event.target) {
    const id = event.target.id.replace("onderzoek-id-", "");
    const type = window.location.hash.replace("#", "");
    const clickedResearch = lastResponse[type].filter((element) => {
      if (element.id == id) {
        return true;
      }
      return false;
    });
    $.ajax({
      url: `http://${DOMINE_NAME}:5000/ervaringsdeskundige/uitschrijven_onderzoek`,
      method: "POST",
      // jsonp: true,
      contentType: "application/json",
      data: JSON.stringify(clickedResearch[0]),
    })
      .done((response) => {
        $(`#list-element-${clickedResearch[0].id}`).remove();
        setTimeout(() => {
          lastResponse[type] = lastResponse[type].filter((element) => {
            return clickedResearch[0].id !== element.id;
          });
          alert("U bent uitgeschreven");
        }, 100);
      })
      .fail((error) => {
        alert("Er is iets misgegaan! Probeer het later opnieuw");

      });
  }
}

function deelname(event) {
  if (event && event.target) {
    const id = event.target.id.replace("onderzoek-id-", "");
    const clickedResearch = lastResponse.beschikbaar.filter((element) => {
      if (element.id == id) {
        return true;
      }
      return false;
    });
    $.ajax({
      url: `http://${DOMINE_NAME}:5000/ervaringsdeskundige/inschrijven_onderzoek`,
      method: "POST",
      // jsonp: true,
      contentType: "application/json",
      data: JSON.stringify(clickedResearch[0]),
    })
      .done((response) => {
       
        $(`#list-element-${clickedResearch[0].id}`).remove();
        setTimeout(() => {
          alert("Dank u wel u bent ingeschreven");
          lastResponse.beschikbaar = lastResponse.beschikbaar.filter(
            (element) => {
              return clickedResearch[0].id !== element.id;
            }
          );
        }, 100);
      })
      .fail((error) => {
        alert("Er is iets misgegaan! Probeer het later opnieuw");
      });
  }
}
$(document).ready(() => {
  getResearches();
  // $("#beschikbaar-href").on("click", () => {
  //   console.log("beschikbaar clicked");
  //   $("#geregisteered").css({ display: "none" });
  //   $("#beschikbaar").css({ display: "block" });
  //   clearInterval(interval);
  //   interval = setInterval(() => {
  //     getResearches();
  //   }, INTERVAL_TIME);
  // });
  // $("#geregisteered-href").on("click", () => {
  //   console.log("geregisteered clicked");
  //   $("#geregisteered").css({ display: "block" });
  //   $("#beschikbaar").css({ display: "none" });
  //   clearInterval(interval);
  //   interval = setInterval(() => {
  //     getResearches("geregisteered");
  //   }, INTERVAL_TIME);
  // });
  function hideTab(tabsID = []) {
    for (let i = 0; i < tabsID.length; i++) {
      $(`#${tabsID[i]}`).css({ display: "none" });
    }
  }

  const TAB_LIST = ["beschikbaar", "goedgekeurd", "afgekeurde", "afwachting"];
  for (let i = 0; i < TAB_LIST.length; i++) {
    const tab = TAB_LIST[i];
    $(`#${tab}-href`).on("click", () => {
      getResearches(tab);
      $(`#${tab}`).css({ display: "block" });
      // hIDE ALL OTHER TABES
      hideTab(TAB_LIST.filter((ele) => tab !== ele));
      clearInterval(interval);
      interval = setInterval(() => {
        getResearches(tab);
      }, INTERVAL_TIME);
    });
  }
  $(`#${TAB_LIST[0]}-href`).click();
});
