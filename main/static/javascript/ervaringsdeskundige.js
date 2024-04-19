var lastResponse = {
  // beschikbaar: null,
  // geregisteered: null,
  // afgekeurde: null,
  // afwachting: null
};
var interval;
var INTERVAL_TIME = 5000;
function getResearches (type = 'beschikbaar') {
  $.ajax({
    url: `http://127.0.0.1:5000/ervaringsdeskundige/haal_onderzoek/${type}`,
    method: "GET",
  })
    .then((jsonResponse) => {
      if (jsonResponse.length > 0) {
        console.log(jsonResponse);
        console.log(JSON.stringify(jsonResponse) == JSON.stringify(lastResponse[type]))
        if (JSON.stringify(jsonResponse) !== JSON.stringify(lastResponse[type])) {
          console.log("response");
          lastResponse[type] = jsonResponse;
          console.log(lastResponse, lastResponse[type].length)
          $(`#aantal-${type}-onderzoeken`).text(lastResponse[type].length)
          console.log({ lastResponse });
          let listItems = '';
          researchtype = type;
          lastResponse[type].forEach((element, index) => {
            let typeButton = type == 'beschikbaar' ? `<button  onclick='deelname(event)'
                          id=onderzoek-id-${element.id}
                          type="button" class="btn btn-primary">Inschrijven</button>
                         ` : `<button  onclick='uitschrijven(event, researchtype)'
                          id=onderzoek-id-${element.id}
                          type="button" class="btn btn-danger">Uitschrijven</button>
                         `

            listItems += `<li class='list-element' id='list-element-${element.id}'><span><i> ${index + 1} <i/> ${element.titel} </span>
                          <div>
                              <p><b>Beschrijving: </b>${element.beschrijving}</p>
                              <p><b>Beschikbaar van:</b> ${element.datum_vanaf} <b>tot:</b> ${element.datum_tot}</p>
                              <p><b>Onderzoekstype: </b>${element.type_onderzoek}</p>
                              <p><b>Locatie: </b>${element.locatie}</p>
                              <p><b>Leeftijds doelgroep: </b>${element.doelgroep_leeftijd_van}-${element.doelgroep_leeftijd_tot}</p>
                              <p><b>Beperking doelgroep: </b>${element.doelgroep_beperking}</p>
                              <p><b>Onderzoek van: </b>${element.organisatie_id}</p>
                              <p><b>Met beloning: </b>${element.met_beloning}</p>
                              <p><b>Beloning(indien van toepassing): </b>${element.beloning}</p>
                              <div id="status_button"><button id="status${element.inschrijving_ervaringsdeskundige_onderzoek_status}"> status: ${element.inschrijving_ervaringsdeskundige_onderzoek_status} </button></div>
                          </div>${typeButton}</li>`
          });
          $(`#list-${type}`).html(listItems);
          if(type == "alle") { 
            $(`*#status_button`).css({'display': "block" });
            $('*#statusnieuw').css({'background-color': 'yellow'});
            $('*#statusgoedgekeurd').css({'background-color': 'greenyellow'});
            $('*#statusafgekeurd').css({'background-color': 'red'});
          }
          else { $(`*#status_button`).css({display: "none" })};
          return
        }
      } else {
        $(`#list-${type}`).html(`<li> Geen onderzoeken gevonden </li>`);
        return
      }
    })
    .catch((error) => { });
    return
};

function uitschrijven(event, type) {
  const resultConfirm = confirm("Weet u het zeker? ");
  console.log({ resultConfirm });
  if (event && event.target) {
    const id = event.target.id.replace('onderzoek-id-', '');
    console.log(type, event);

    if (type ==  "nieuw"){response = lastResponse.nieuw}
    else if(type == "goedgekeurd"){response = lastResponse.goedgekeurd}
    else if(type == "afgekeurd"){response = lastResponse.afgekeurd}
    else if(type == "alle"){response=lastResponse.alle}
    
    const clickedResearch = response.filter((element) => {
      if (element.id == id) {
        return true;
      }
      return false;
    });

    console.log({ clickedResearch });
    $.ajax({
      url: "http://127.0.0.1:5000/ervaringsdeskundige/uitschrijven_onderzoek",
      method: "POST",
      // jsonp: true,
      contentType: "application/json",
      data: JSON.stringify(clickedResearch[0]),
    })
      .done((response) => {
        console.log(response);
        console.log(event.target.id)
        $(`#list-element-${clickedResearch[0].id}`).remove();
        alert('U bent uitgeschreven')
      })
      .fail((error) => {
        alert("Er is iets misgegaan! Probeer het later opnieuw");
        console.error(error);
      });
  }
}

function deelname(event) {
  if (event && event.target) {
    const id = event.target.id.replace("onderzoek-id-", "");
    console.log(id);
    console.log(lastResponse);
    const clickedResearch = lastResponse.beschikbaar.filter((element) => {
      if (element.id == id) {
        return true;
      }
      return false;
    });
    console.log({ clickedResearch });
    $.ajax({
      url: "http://127.0.0.1:5000/ervaringsdeskundige/inschrijven_onderzoek",
      method: "POST",
      // jsonp: true,
      contentType: "application/json",
      data: JSON.stringify(clickedResearch[0]),
    })
      .done((response) => {
        console.log(response);
        console.log(`#list-element-${clickedResearch[0].id}`)
        console.log($(`#list-element-${clickedResearch[0].id}`))
        $(`#list-element-${clickedResearch[0].id}`).remove();
        alert('Dank u wel u bent ingeschreven')
      })
      .fail((error) => {
        alert("Er is iets misgegaan! Probeer het later opnieuw");
        console.error(error);
      });
  }
}
$(document).ready(() => {
  const TAB_LIST = ["beschikbaar", "goedgekeurd", "nieuw", "afgekeurd", "alle"];
  hideTab(TAB_LIST)
  for (let i = 0; i < TAB_LIST.length; i++) {
    const tab = TAB_LIST[i];
    $(`#${tab}-href`).on("click", () => {
      console.log(`#${tab}-href`);
      if(tab == "alle") { $(`*#status_button`).css({display: "block" })}
      else { $(`*#status_button`).css({display: "none" })};
      getResearches(tab)
      $(`#${tab}`).css({ display: "block" });
      // hIDE ALL OTHER TABES
      hideTab(TAB_LIST.filter((ele) => tab !== ele));
      clearInterval(interval);
      interval = setInterval(() => {
        getResearches(tab);
      }, INTERVAL_TIME);
    });
  }
});
function hideTab(tabsID = []) {
  for (let i = 0; i < tabsID.length; i++) {
    $(`#${tabsID[i]}`).css({ display: "none" });
  }
}