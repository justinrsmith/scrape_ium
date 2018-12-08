<?
define( 'WP_USE_THEMES', false );
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-config.php';
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-load.php';
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-admin/includes/taxonomy.php';
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-includes/pluggable.php';
include_once '/Users/justinsmith/projects/illinois-urban-manual/advanced-custom-fields/acf.php';


$dir = "pdfs/*";
$wp_upload_dir = wp_upload_dir();
foreach(glob($dir) as $file) {  
  

// // Get the path to the upload directory.
// $wp_upload_dir = wp_upload_dir();

// foreach($images as $name) {
    $attachment = array(
        'guid'=> $wp_upload_dir['url'] . '/' . basename( $file ), 
        'post_mime_type' => 'image/png',
        'post_title' => 'my description',
        'post_content' => 'my description',
        'post_status' => 'inherit'
         );

    $image_id = wp_insert_attachment($attachment, $file);

    // Make sure that this file is included, as wp_generate_attachment_metadata() depends on it.
    require_once( '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-admin/includes/image.php' );
 
    // Generate the metadata for the attachment, and update the database record.
    $attach_data = wp_generate_attachment_metadata( $image_id, $file );

    wp_update_attachment_metadata( $image_id, $attach_data );

}


?>