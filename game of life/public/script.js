const cube = ([x,y,z]) => [[x,y,z],[x,y,z+1],[x,y+1,z],[x,y+1,z+1],
                           [x+1,y,z],[x+1,y,z+1],[x+1,y+1,z],[x+1,y+1,z+1]],  
      add_vec_to_list = (list, vec) => list.map((e)=>e.map((c,i)=>c+vec[i]));
      size = 100; 
const shapes = {
  "stable-4": [[3,3,3],[3,3,2],[3,2,3],[3,2,2],
           [2,3,3],[2,3,2],[2,2,3],[2,2,2]],
  "stable-3": [[3,3,3],[3,3,2],[3,2,3],[3,2,2],
           [2,3,3],[2,3,2],[2,2,3],[2,2,2],
            [1,1,1],[1,1,22],[1,22,1],[1,22,22],
           [22,1,1],[22,1,22],[22,22,1],[22,22,22]],
  "stable-1": cube([3,3,3]).concat(cube([1,3,3])).concat(cube([1,1,3])),
  "explosion": [[3,3,3],[3,1,1],[3,3,1],[1,3,1]].concat(cube([4,4,4])).concat(cube([4,4,1])).concat(cube([4,1,4])).concat(cube([4,1,1]))
              .concat(cube([1,4,4])).concat(cube([1,4,1])).concat(cube([1,1,4])).concat(cube([1,1,1])),
  "fail-1": [[3,3,3],[3,3,2],[3,2,3],[3,2,2],
           [2,3,3],[2,3,2],[2,2,3],[2,2,2],[4,4,4],[1,1,1]],
  "test": [[3,3,3],[3,3,2],[3,2,3],[3,2,2],[4,4,1],[1,1,4],
           [2,3,3],[2,3,2],[2,2,3],[2,2,2],[4,4,4],[1,1,1]]
},
  obj = add_vec_to_list(shapes["explosion"],[size/2,size/2,size/2]);
function zeros(dimensions) {
    var array = [];

    for (var i = 0; i < dimensions[0]; ++i) {
        array.push(dimensions.length == 1 ? 0 : zeros(dimensions.slice(1)));
    }

    return array;
}
let cells = zeros([size,size,size]),
    watchmap = new WeakMap(),
    watchlist = [],
    init = false,
    mat;
$(function(){
  //100 x 100 x 100 array
  let scene = new THREE.Scene(),
      camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 ),
      renderer = new THREE.WebGLRenderer();
  renderer.setSize( window.innerWidth, window.innerHeight );
  $('body').append( renderer.domElement );
  var geometry = new THREE.BoxGeometry( 1, 1, 1 );
  var material = new THREE.MeshNormalMaterial( { color: 0x00ff00 } );
  mat = () => material;
  var cubes = new THREE.Object3D();
  var controls = new THREE.OrbitControls(camera);
  function animate(){}
  controls.addEventListener( 'change', animate );
  scene.add(cubes);
  var directionalLight = new THREE.DirectionalLight( 0xffffff, 0.5 );
  scene.add( directionalLight );
  
  for (let [x,y,z] of obj) {
    console.log(x,y,z)
    let cb = new THREE.Mesh(geometry, mat());
    cb.position.set(x-size/2,y-size/2,z-size/2);
    cubes.add( cb );
    for (let i = -1; i <= 1; i++){

      for (let j = -1; j <= 1; j++){
        
        for (let k = -1; k <= 1; k++){

          watchmap[[x+i,y+j,z+k]] = true;
          watchlist.push([x+i,y+j,z+k]);

        }

      }

    }
    cells[x][y][z] = cb;
  }
  camera.position.z = 10;
  
  const watch_all_neighbors = ([x,y,z], arr, wm) => {
    
    for (let i = -1; i <= 1; i++){

      for (let j = -1; j <= 1; j++){
        
        for (let k = -1; k <= 1; k++){

          wm[[x+i,y+j,z+k]] = true;
          arr.push([x+i,y+j,z+k]);

        }

      }

    }

  },
  mod = (x,y) => ((x%y)+y)%y,
  safe_lookup = (arr, ...args) => {
    if(args.length == 0){
      return arr
    }
    return safe_lookup(arr[mod(args.shift(),arr.length)],...args);     
  }
  function update(){
    let changes = [],
        new_watchlist = [],
        new_wm = new WeakMap();
    for (let pos of watchlist) {
      let [i,j,k] = pos;
      i = mod(i, cells.length);
      j = mod(j, cells[i].length);
      k = mod(k, cells[i][j].length);
      if (watchmap[pos] == true) {
        watchmap[pos] = false;
        var self = safe_lookup(cells, i, j, k)?1:0,
            sum = -self; //account for counting the cell itself

        for (var x = -1; x < 2; x++){
          for (var y = -1; y < 2; y++){
            for (var z = -1; z < 2; z++){
              sum += (safe_lookup(cells, i+x, j+y, k+z)?1:0);
            }
          } 
        }

        if(self){
          if(sum < 4){
            console.log('lonely: ',pos,sum)
            changes.push([i,j,k,0]);
            watch_all_neighbors(pos,new_watchlist,new_wm);
          }
          if(sum > 7){
            changes.push([i,j,k,0]);
            watch_all_neighbors(pos,new_watchlist,new_wm);
          }
        }
        else if((sum==5)){
          changes.push([i,j,k,1]);
          watch_all_neighbors(pos,new_watchlist,new_wm);
        }
      }
    }
    console.log('Watchlist and new%', watchlist, new_watchlist)
    watchlist = new_watchlist;
    watchmap = new_wm;
    return changes;
  }
  function animate() {
    //let changes = update();
    /*
    for (let pt of changes) {
      let cb = new THREE.Mesh(geometry, material);
      cb.position.set(...pt);
      scene.add( cb );
      console.log(cb);
    }
    */
    renderer.render( scene, camera );
  }
  animate();
  
  $('body').on('keydown', (e)=>{
    if(e.which == 32){
      let changes = update();
      for (let [i,j,k,t] of changes) {
        if(t==0){
          cubes.remove(cells[i][j][k])
          //delete cells[i][j][k];
          cells[i][j][k] = 0;
        }
        else if(t==1){
          let cb = new THREE.Mesh(geometry, mat());
          cb.position.set(i-size/2,j-size/2,k-size/2)
          cubes.add(cb)
          cells[i][j][k] = cb;
        }else {
          console.log(t)
        }
      }
      animate();
    }
  })
});