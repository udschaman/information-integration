$(function() {
   Morris.Bar({
        element: 'state-bar-chart',
        data: [{ state: 'Alabama', sightings: 847},{ state: 'Alaska', sightings: 442},{ state: 'Arizona', sightings: 3345},{ state: 'Arkansas', sightings: 748},{ state: 'California', sightings: 11487},{ state: 'Colorado', sightings: 1905},{ state: 'Connecticut', sightings: 1234},{ state: 'Delaware', sightings: 236},{ state: 'District Of Columbia', sightings: 121},{ state: 'Florida', sightings: 5129},{ state: 'Georgia', sightings: 1758},{ state: 'Hawaii', sightings: 358},{ state: 'Idaho', sightings: 793},{ state: 'Illinois', sightings: 3133},{ state: 'Indiana', sightings: 1717},{ state: 'Iowa', sightings: 884},{ state: 'Kansas', sightings: 804},{ state: 'Kentucky', sightings: 1099},{ state: 'Louisiana', sightings: 773},{ state: 'Maine', sightings: 752},{ state: 'Maryland', sightings: 1167},{ state: 'Massachusetts', sightings: 1781},{ state: 'Michigan', sightings: 2468},{ state: 'Minnesota', sightings: 1139},{ state: 'Mississippi', sightings: 529},{ state: 'Missouri', sightings: 1846},{ state: 'Montana', sightings: 669},{ state: 'Nebraska', sightings: 480},{ state: 'Nevada', sightings: 1074},{ state: 'New Hampshire', sightings: 692},{ state: 'New Jersey', sightings: 1681},{ state: 'New Mexico', sightings: 1014},{ state: 'New York', sightings: 3959},{ state: 'North Carolina', sightings: 2411},{ state: 'North Dakota', sightings: 177},{ state: 'Ohio', sightings: 2825},{ state: 'Oklahoma', sightings: 927},{ state: 'Oregon', sightings: 2354},{ state: 'Pennsylvania', sightings: 3123},{ state: 'Puerto Rico', sightings: 25},{ state: 'Rhode Island', sightings: 373},{ state: 'South Carolina', sightings: 1384},{ state: 'South Dakota', sightings: 252},{ state: 'Tennessee', sightings: 1543},{ state: 'Texas', sightings: 4291},{ state: 'Utah', sightings: 819},{ state: 'Vermont', sightings: 369},{ state: 'Virginia', sightings: 1752},{ state: 'Virgin Islands', sightings: 1},{ state: 'Washington', sightings: 4921},{ state: 'West Virginia', sightings: 609},{ state: 'Wisconsin', sightings: 1636},{ state: 'Wyoming', sightings: 234}],
        xkey: 'state',
        ykeys: ['sightings'],
        labels: ['Sightings'],
        barRatio: 0.4,
        xLabelAngle: 35,
        hideHover: 'auto',
        resize: true
    });
});