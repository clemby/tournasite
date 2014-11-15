function formatApiResponse(data) {
  var fixtures = [],
      results = [];

  $.each(data.matches, function(i, match) {
    var a = match.teams.slice();
    a.push(match.name);
    fixtures.push(a);

    var result;
    if (match.winner) {
      switch ($.inArray(match.winner, match.teams)) {
        case 0:
          result = [1, 0];
          break;
        case 1:
          result = [0, 1];
          break;
        default:
          throw Error("Couldn't find match winner among teams!");
      }
    }
    else {
      result = null;
    }

    results.push(result);
  });

  var teams = $.map(data.teams, function(team) { 
    return team.name;
  });

  return {
    teams: teams,
    fixtures: fixtures,
    results: results
  };
}


function setupBrackets(elem, data) {
  var formatted = formatApiResponse(data);

  $(elem).bracket({
    init: {
      teams: formatted.fixtures,
      results: formatted.results
    }
  });
}
