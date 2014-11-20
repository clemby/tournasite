function formatApiResponse(data) {
  var teams = {},
      matches = {},
      heads = [];

  $.each(data.teams, function(i, team) {
    teams[team.id] = team;
  });

  $.each(data.matches, function(i, match) {
    matches[match.id] = match;

    if (typeof match.winnerNext !== 'number') {
      heads.push(match.id);
    }
  });


  // 'Head': final or, if a double elimination, losing bracket final.
  var headCount = heads.length;
  if (!headCount) {
    throw Error("Empty or circular tournament");
  }

  if (headCount > 2) {
    throw Error("Too many tournament heads");
  }


  var trees = heads.map(getTree).sort(function(a, b) {
    return b.length - a.length;
  });

  var results = trees.map(function(tree) {
    return tree.map(function(tier) {
      return tier.map(getResult);
    });
  });

  var firstFixtures = trees[0][0];
  var firstFixtureTeams = firstFixtures.map(function(matchId) {
    return matches[matchId].teams.map(function(teamId) {
      return teams[teamId].name;
    });
  });


  return {
    teams: firstFixtureTeams,
    matches: matches,
    results: results,
    trees: trees
  };

  function isEmpty(obj) {
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        return false;
      }
    }
    return true;
  }


  function getTree(head) {
    var currentTier = [head],
        tiers = [];

    while (currentTier.length) {
      tiers.push(currentTier);
      currentTier = $.map(currentTier, function(matchId) {
        return getChildren(matchId);
      });
    }

    return tiers.reverse();
  }


  function getChildren(parentId) {
    return $.map(matches, function(match) {
      return match.winnerNext === parentId ? match.id : null;
    });
  }


  function getResult(matchId) {
    var match = matches[matchId];

    if (typeof match.winner !== 'number') {
      return null;
    }

    switch ($.inArray(match.winner, match.teams)) {
      case 0:
        return [1, 0];
      case 1:
        return [0, 1];
      default:
        throw Error("Can't find match winner among participants!");
    }
  }
}


function setupBrackets(elem, data) {
  var formatted = formatApiResponse(data);

  $(elem).bracket({
    init: {
      teams: formatted.teams,
      results: [formatted.results[0]]
    }
  });
}
