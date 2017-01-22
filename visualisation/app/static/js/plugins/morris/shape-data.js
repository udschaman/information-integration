$(function() {

    Morris.Bar({
        element: 'shape-bar-chart',
        data: [{ shape: 'other', sightings: 14506},{ shape: 'cigar', sightings: 2056},{ shape: 'round', sightings: 2},{ shape: 'flare', sightings: 1},{ shape: 'diamond', sightings: 1223},{ shape: 'sphere', sightings: 5592},{ shape: 'fireball', sightings: 6891},{ shape: 'delta', sightings: 7},{ shape: 'triangle', sightings: 8350},{ shape: 'teardrop', sightings: 761},{ shape: 'light', sightings: 17638},{ shape: 'cross', sightings: 272},{ shape: 'crescent', sightings: 1},{ shape: 'hexagon', sightings: 1},{ shape: 'flash', sightings: 1491},{ shape: 'changing', sightings: 2120},{ shape: 'oval', sightings: 3854},{ shape: 'formation', sightings: 2634},{ shape: 'pyramid', sightings: 1},{ shape: 'cylinder', sightings: 1323},{ shape: 'chevron', sightings: 1024},{ shape: 'cone', sightings: 341},{ shape: 'rectangle', sightings: 1416},{ shape: 'disk', sightings: 5188},{ shape: 'circle', sightings: 8675},{ shape: 'egg', sightings: 722}],
        xkey: 'shape',
        ykeys: ['sightings'],
        labels: ['Sightings'],
        barRatio: 0.4,
        xLabelAngle: 35,
        hideHover: 'auto',
        resize: true
    });


});
