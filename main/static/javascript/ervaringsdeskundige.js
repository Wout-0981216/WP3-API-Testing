var lastResponse = {
  // beschikbaar: null,
  // geregisteered: null,
  // afgekeurde: null,
  // afwachting: null
};
var interval;
var INTERVAL_TIME = 5000;
const getResearches = (type = 'beschikbaar') => {
  $.ajax({
    url: `http://127.0.0.1:5000/ervaringsdeskundige/haal_onderzoek/${type}`,
    method: "GET",
  })
    .then((jsonResponse) => {
      if (jsonResponse.length > 0) {
        console.log(jsonResponse);
        console.log(JSON.stringify(jsonResponse) !== JSON.stringify(lastResponse[type]))
        if (JSON.stringify(jsonResponse) !== JSON.stringify(lastResponse[type])) {
          console.log("response");
          lastResponse[type] = jsonResponse;
          console.log(lastResponse, lastResponse[type].length)
          $(`#aantal-${type}-onderzoeken`).text(lastResponse[type].length)
          console.log({ lastResponse });
          let listItems = '';
          lastResponse[type].forEach((element, index) => {
            let typeButton = type == 'beschikbaar' ? `<button  onclick='deelname(event)'
                          id=onderzoek-id-${element.id}
                          type="button" class="btn btn-primary">Inschrijven</button>
                         ` : `<button  onclick='uitschrijven(event)'
                          id=onderzoek-id-${element.id}
                          type="button" class="btn btn-danger">Uitschrijven</button>
                         `

            listItems += `<li class='list-element' id='list-element-${element.id}'>
                          <span><i> ${index + 1} <i/> ${element.titel} </span>
                          <div>
                              <p>${element.beschrijving}</p>
                          </div>
                          ${typeButton}
                          </li>`
          });
          $(`#list-${type}`).html(listItems);
        }
      } else {
        $(`#list-${type}`).html(`<li>No Research found </li>`);
      }
    })
    .catch((error) => { });
};

function uitschrijven() {
  const resultConfirm = confirm("Bent u zeker! ");
  console.log({ resultConfirm });
  if (event && event.target) {
    const id = event.target.id.replace('onderzoek-id-', '');
    console.log(id);
    const clickedResearch = lastResponse.geregisteered.filter((element) => {
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
  getResearches()
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

  const TAB_LIST = ["beschikbaar", "geregisteered", "afgekeurde", "afwachting"];
  for (let i = 0; i < TAB_LIST.length; i++) {
    const tab = TAB_LIST[i];
    $(`#${tab}-href`).on("click", () => {
      console.log(`#${tab}-href`);
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
  $(`#${TAB_LIST[0]}-href`).click();
});