$(document).ready( function() {
    $( "ul.sortable" ).sortable({
        update: function(event, ui) {
            updateOrder();
        }
    });
    $( "li.draggable" ).draggable({
        connectToSortable: ".sortable",
        revert: "invalid"
    });
    $( "ul, li" ).disableSelection();
} );
function updateOrder() {
    var item_order = new Array();
    $('ul.sortable li').each(function(){
        item_order.push($(this).attr("id"));
    })
}