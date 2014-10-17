/* Try to highlight the working section in the navbar
/* $(document).ready(function(){
    $('.nav li').click(function(e) {
        $('.nav li').removeClass('active');
        var $this = $(this);
        if (!$this.hasClass('active')) {
            $this.addClass('active');
        }
        e.preventDefault();
    });
});
*/

// Species toggle
// all species
$('#select-all').click(function() {
$('.org input[name^="org"]').each(function(){
    $(this).prop('checked',!$(this).prop('checked'));
});
});

// vertebrate
$('#select-vertebrate').click(function() {
$('.org input[name^="org:vertebrate"]').each(function(){
    $(this).prop('checked',!$(this).prop('checked'));
});
});

// invertebrate
$('#select-invertebrate').click(function() {
$('.org input[name^="org:invertebrate"]').each(function(){
    $(this).prop('checked',!$(this).prop('checked'));
});
});

// unicellular
$('#select-unicellular').click(function() {
$('.org input[name^="org:unicellular"]').each(function(){
    $(this).prop('checked',!$(this).prop('checked'));
});
});

// [typeahead] human gene
//var hg_names = ['PHP', 'MySQL', 'SQL', 'PostgreSQL', 'HTML', 'CSS', 'HTML5', 'CSS3', 'JSON'];
//$('#human_gene_name').typeahead( {source: hg_names, minLength: 2} );
$('#human_gene_name').typeahead({
    source: function (query, process) {
        return $.get('static/json/human_gene_name.json', { query: query }, function (data) {
            return process(data.genename);
        });
    }
});

// [typeahead] domain name
$('#domain_name').typeahead({
    source: function (query, process) {
        return $.get('static/json/domain_name.json', { query: query }, function (data) {
            return process(data.domainname);
        });
    }
});

// [typeahead] superfamily
$('#superfam_name').typeahead({
    source: function (query, process) {
        return $.get('static/json/superfam_name.json', { query: query }, function (data) {
            return process(data.superfam);
        });
    }
});

// [typeahead] family
$('#fam_name').typeahead({
    source: function (query, process) {
        return $.get('static/json/fam_name.json', { query: query }, function (data) {
            return process(data.mfam);
        });
    }
});

// [typeahead] subfamily
$('#subfam_name').typeahead({
    source: function (query, process) {
        return $.get('static/json/subfam_name.json', { query: query }, function (data) {
            return process(data.subfam);
        });
    }
});





