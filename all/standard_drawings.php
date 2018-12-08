<?
define( 'WP_USE_THEMES', false );
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-config.php';
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-load.php';
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-admin/includes/taxonomy.php';
require_once '/Users/justinsmith/projects/illinois-urban-manual/wordpress/wp-includes/pluggable.php';
include_once '/Users/justinsmith/projects/illinois-urban-manual/advanced-custom-fields/acf.php';

function wp_get_attachment_by_post_name( $post_name ) {
    $args = array(
        'posts_per_page' => 1,
        'post_type'      => 'attachment',
        'name'           => trim ( $post_name ),
    );
    $get_attachment = new WP_Query( $args );

    if ( $get_attachment->posts[0] )
        return $get_attachment->posts[0];
    else
      return false;
}

$csvFile = file('csvs/standard_drawings.csv');
$data = [];
foreach ($csvFile as $line) {
    $data[] = str_getcsv($line);
}
foreach ($data as $row) {
    $now = new \DateTime();
    $now->setTimezone(new DateTimeZone('America/Chicago'));
    $now = $now->format('Y-m-d H:i:s');
    $id = wp_insert_post(array(
        'post_title'    => $row[0],
        'post_date'     => $now,
        'post_type'     => 'standard_drawings',
        'post_status'   => 'publish',
    ));
    if ($id) {
        var_dump(wp_get_attachment_by_post_name($row[2]));
        echo $row[2];
        update_field( 'field_5af9848475e11', $row[0], $id );
        update_field( 'field_5af984d775e13', $row[1], $id );
        update_field( 'field_5af9ef193e969',  wp_get_attachment_by_post_name($row[2]), $id );
    } else {
        echo 'fail';
    }
}
?>