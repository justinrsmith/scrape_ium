( function($) {

    $( '.header-search-button' ).click( function() {
        $( '.header-search' ).toggleClass( 'header-search-open' );
        $( '.navbar-collapse').removeClass( 'in' ).attr( 'aria-expanded', 'false' ).css( 'height', '1px' );
        $( '.navbar-toggle').attr( 'aria-expanded', 'false' );
        $( '.navbar-toggle').addClass( 'collapsed' );
    } );

    $( '.header-search' ).click( function(event) {
        event.stopPropagation();
    } );

    $( 'html' ).click( function() {
        $( '.header-search' ).removeClass( 'header-search-open' );
    } );
    
} )(jQuery);