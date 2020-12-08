var now = new Date();
  const urlParams = new URLSearchParams(window.location.search);
  const salesMonthParam = parseInt(urlParams.get('salesMonth')) || now.getMonth() + 1;
  const salesYearParam = parseInt(urlParams.get('salesYear')) || now.getFullYear();
  const usedMonthParam = parseInt(urlParams.get('usedMonth')) || now.getMonth() + 1;
  const usedYearParam = parseInt(urlParams.get('usedYear')) || now.getFullYear();

function nextsale() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(salesMonth + 1 > 12) {
    $('#salesYear').val(++salesYear)
    salesMonth = 0
    $('#salesMonth').val(salesMonth)
  }

  $('#salesMonth').val(salesMonth+1)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}

function nextused() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(usedMonth + 1 > 12) {
    $('#salesYear').val(++usedYear)
    usedMonth = 0
    $('#salesMonth').val(usedMonth)
  }
  $('#salesMonth').val(salesMonth)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth+1)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}

function backsale() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(salesMonth - 1 < 1) {
    $('#salesYear').val(--salesYear)
    salesMonth = 13
    $('#salesMonth').val(salesMonth)
  }

  $('#salesMonth').val(salesMonth-1)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}

function backused() {
  var salesMonth = salesMonthParam
  var salesYear = salesYearParam
  var usedMonth = usedMonthParam
  var usedYear = usedYearParam
  if(usedMonth - 1 < 1) {
    $('#salesYear').val(--usedYear)
    usedMonth = 13
    $('#salesMonth').val(usedMonth)
  }
  $('#salesMonth').val(salesMonth)
  $('#salesYear').val(salesYear)

  $('#usedMonth').val(usedMonth - 1)
  $('#usedYear').val(usedYear)
  $('#formDate').submit()
}