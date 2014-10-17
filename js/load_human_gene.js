// [typeahead] human gene name
/*
$(document).ready(function() {
  $('#human_gene').typeahead({
    source: function (query, process) {
        return $.get('/static/json/human_gene_name.json', { query: query }, function (data) {
            return process(data.genename);
        });
    }
  });
});
*/

$(document).ready(function() {
  $('#human_gene').typeahead({
    source: function (query, process) {
        return $.get('/static/json/human_gene_name.json', { query: query }, function (data) {
            return process(data.genename);
        });
    }
  });
});