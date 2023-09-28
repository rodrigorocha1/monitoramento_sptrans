import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title='Monitoramento sptrans'
)

st.write('Mapa')
posicao = [[-23.563552856445312, -46.59136199951172],
           [-23.563457489013672, -46.59130096435547],
           [-23.563152313232422, -46.59112548828125],
           [-23.56327247619629, -46.59102249145508],
           [-23.562679290771484, -46.59071350097656],
           [-23.563173294067383, -46.589637756347656],
           [-23.56354522705078, -46.58881759643555],
           [-23.563753128051758, -46.58834457397461],
           [-23.5639705657959, -46.58787536621094],
           [-23.564361572265625, -46.5870246887207],
           [-23.564401626586914, -46.58692169189453],
           [-23.564531326293945, -46.586639404296875],
           [-23.564611434936523, -46.586463928222656],
           [-23.564966201782227, -46.58568572998047],
           [-23.56502914428711, -46.585514068603516],
           [-23.56557846069336, -46.585567474365234],
           [-23.565752029418945, -46.58558654785156],
           [-23.566030502319336, -46.58560562133789],
           [-23.566450119018555, -46.58563995361328],
           [-23.56669044494629, -46.585662841796875],
           [-23.566835403442383, -46.58567428588867],
           [-23.567049026489258, -46.5857048034668],
           [-23.567276000976562, -46.58571243286133],
           [-23.567283630371094, -46.58464050292969],
           [-23.56728744506836, -46.583621978759766],
           [-23.567304611206055, -46.58264923095703],
           [-23.56730842590332, -46.58247375488281],
           [-23.568618774414062, -46.58257293701172],
           [-23.568408966064453, -46.581703186035156],
           [-23.568344116210938, -46.581424713134766],
           [-23.568063735961914, -46.58027267456055],
           [-23.567455291748047, -46.58021545410156],
           [-23.567047119140625, -46.580177307128906],
           [-23.566377639770508, -46.580116271972656],
           [-23.566164016723633, -46.58009338378906],
           [-23.56610870361328, -46.5800895690918],
           [-23.565988540649414, -46.580074310302734],
           [-23.565887451171875, -46.58005142211914],
           [-23.565711975097656, -46.57996368408203],
           [-23.56561279296875, -46.57990646362305],
           [-23.56553840637207, -46.57985305786133],
           [-23.565427780151367, -46.579776763916016],
           [-23.565256118774414, -46.57963943481445],
           [-23.565147399902344, -46.57951736450195],
           [-23.564790725708008, -46.579349517822266],
           [-23.56415557861328, -46.579044342041016],
           [-23.56396484375, -46.57896041870117],
           [-23.563615798950195, -46.578800201416016],
           [-23.563396453857422, -46.57868576049805],
           [-23.56321907043457, -46.57855987548828],
           [-23.56298828125, -46.578372955322266],
           [-23.562803268432617, -46.578182220458984],
           [-23.562713623046875, -46.57802963256836],
           [-23.562644958496094, -46.57793045043945],
           [-23.56226921081543, -46.57883834838867],
           [-23.56192970275879, -46.57970428466797],
           [-23.561864852905273, -46.58050537109375],
           [-23.561840057373047, -46.58083724975586],
           [-23.561830520629883, -46.58094787597656],
           [-23.56182098388672, -46.58102035522461],
           [-23.561817169189453, -46.581119537353516],
           [-23.561752319335938, -46.581974029541016],
           [-23.561702728271484, -46.58271026611328],
           [-23.561660766601562, -46.58311080932617],
           [-23.5616397857666, -46.58324432373047],
           [-23.561260223388672, -46.58412170410156],
           [-23.560850143432617, -46.58500289916992],
           [-23.56061553955078, -46.584983825683594],
           [-23.56038475036621, -46.58497619628906],
           [-23.560317993164062, -46.58497619628906],
           [-23.56022071838379, -46.584983825683594],
           [-23.55948829650879, -46.58503723144531],
           [-23.559038162231445, -46.58504867553711],
           [-23.558799743652344, -46.58506393432617],
           [-23.55879020690918, -46.58500671386719],
           [-23.55876922607422, -46.5849609375],
           [-23.558717727661133, -46.58489227294922],
           [-23.558666229248047, -46.58485412597656],
           [-23.558565139770508, -46.58482360839844],
           [-23.55849266052246, -46.58482360839844],
           [-23.558414459228516, -46.584842681884766],
           [-23.558345794677734, -46.584869384765625],
           [-23.558271408081055, -46.58490753173828],
           [-23.558155059814453, -46.584983825683594],
           [-23.557443618774414, -46.5855712890625],
           [-23.557254791259766, -46.585479736328125],
           [-23.55701446533203, -46.58534240722656],
           [-23.556734085083008, -46.58518981933594],
           [-23.55642318725586, -46.58502197265625],
           [-23.556198120117188, -46.58490753173828],
           [-23.555545806884766, -46.58454895019531],
           [-23.5554256439209, -46.58448791503906],
           [-23.554866790771484, -46.58418273925781],
           [-23.554624557495117, -46.58405685424805],
           [-23.554401397705078, -46.58393859863281],
           [-23.554126739501953, -46.58378982543945],
           [-23.554031372070312, -46.583717346191406],
           [-23.553956985473633, -46.58366775512695],
           [-23.55375099182129, -46.583438873291016],
           [-23.553691864013672, -46.5833740234375],
           [-23.55335235595703, -46.58300018310547],
           [-23.5531005859375, -46.58272933959961],
           [-23.552671432495117, -46.58225631713867],
           [-23.552165985107422, -46.58171463012695],
           [-23.55275535583496, -46.58100509643555],
           [-23.552682876586914, -46.58091735839844],
           [-23.551774978637695, -46.58000183105469],
           [-23.551536560058594, -46.57975387573242],
           [-23.551530838012695, -46.57975769042969],
           [-23.55150032043457, -46.57977294921875],
           [-23.551372528076172, -46.5798454284668],
           [-23.55132484436035, -46.579872131347656],
           [-23.550722122192383, -46.58021545410156],
           [-23.55032730102539, -46.580467224121094],
           [-23.550060272216797, -46.58064270019531],
           [-23.54952049255371, -46.58106994628906],
           [-23.548961639404297, -46.58153533935547],
           [-23.548778533935547, -46.58169937133789],
           [-23.548587799072266, -46.5818977355957],
           [-23.548402786254883, -46.58208465576172],
           [-23.547557830810547, -46.58300018310547],
           [-23.547496795654297, -46.583072662353516],
           [-23.54627227783203, -46.584564208984375],
           [-23.544231414794922, -46.58256912231445],
           [-23.543800354003906, -46.58213424682617],
           [-23.543630599975586, -46.58202362060547],
           [-23.543466567993164, -46.58188247680664],
           [-23.543386459350586, -46.581787109375],
           [-23.543285369873047, -46.5816650390625],
           [-23.543210983276367, -46.58153533935547],
           [-23.543170928955078, -46.581363677978516],
           [-23.543149948120117, -46.58126449584961],
           [-23.543123245239258, -46.58102798461914],
           [-23.54311752319336, -46.58091735839844],
           [-23.543107986450195, -46.58073043823242],
           [-23.543100357055664, -46.580509185791016],
           [-23.543094635009766, -46.58035659790039],
           [-23.543094635009766, -46.58030319213867],
           [-23.5430850982666, -46.58013916015625],
           [-23.543075561523438, -46.579872131347656],
           [-23.543071746826172, -46.579708099365234],
           [-23.543079376220703, -46.57958984375],
           [-23.5430965423584, -46.57951354980469],
           [-23.543115615844727, -46.57943344116211],
           [-23.543140411376953, -46.579376220703125],
           [-23.543216705322266, -46.579246520996094],
           [-23.543474197387695, -46.5789794921875],
           [-23.543720245361328, -46.57875061035156],
           [-23.543790817260742, -46.578670501708984],
           [-23.54383659362793, -46.57859802246094],
           [-23.543882369995117, -46.57850646972656],
           [-23.54397964477539, -46.57832717895508],
           [-23.543981552124023, -46.57821273803711],
           [-23.543996810913086, -46.57810974121094],
           [-23.544010162353516, -46.57793426513672],
           [-23.544031143188477, -46.57775115966797],
           [-23.5440731048584, -46.577571868896484],
           [-23.54410743713379, -46.577457427978516],
           [-23.544130325317383, -46.57737350463867],
           [-23.544166564941406, -46.57731246948242],
           [-23.544200897216797, -46.5772590637207],
           [-23.544265747070312, -46.5771484375],
           [-23.54431915283203, -46.57706069946289],
           [-23.54468536376953, -46.57646942138672],
           [-23.544017791748047, -46.57664108276367],
           [-23.543010711669922, -46.57688903808594],
           [-23.54252052307129, -46.577003479003906],
           [-23.542287826538086, -46.57706069946289],
           [-23.542236328125, -46.577091217041016],
           [-23.542224884033203, -46.577117919921875],
           [-23.542213439941406, -46.577152252197266],
           [-23.542402267456055, -46.57798767089844],
           [-23.542354583740234, -46.57803726196289],
           [-23.542316436767578, -46.57808303833008],
           [-23.542095184326172, -46.57814025878906],
           [-23.541582107543945, -46.5782585144043],
           [-23.541507720947266, -46.57829666137695],
           [-23.541461944580078, -46.578067779541016],
           [-23.54127311706543, -46.577571868896484],
           [-23.541156768798828, -46.5772705078125],
           [-23.541105270385742, -46.57714080810547],
           [-23.541080474853516, -46.5770378112793],
           [-23.54104995727539, -46.5768928527832],
           [-23.541027069091797, -46.576778411865234],
           [-23.541013717651367, -46.57670211791992],
           [-23.540987014770508, -46.57658386230469],
           [-23.540973663330078, -46.576515197753906],
           [-23.540950775146484, -46.5764045715332],
           [-23.540939331054688, -46.57634735107422],
           [-23.54092025756836, -46.576255798339844],
           [-23.5408992767334, -46.5761604309082],
           [-23.540876388549805, -46.5760383605957],
           [-23.540855407714844, -46.5759391784668],
           [-23.54082679748535, -46.575809478759766],
           [-23.540807723999023, -46.5756950378418],
           [-23.54079818725586, -46.575645446777344],
           [-23.54079246520996, -46.57561111450195],
           [-23.540790557861328, -46.57556915283203],
           [-23.540790557861328, -46.57553482055664],
           [-23.54081153869629, -46.57550811767578],
           [-23.54084587097168, -46.57548904418945],
           [-23.540882110595703, -46.57548141479492],
           [-23.540910720825195, -46.57548522949219],
           [-23.54093360900879, -46.575496673583984],
           [-23.540958404541016, -46.57551956176758],
           [-23.540969848632812, -46.5755500793457],
           [-23.54100227355957, -46.57570266723633],
           [-23.54102325439453, -46.57581329345703],
           [-23.541053771972656, -46.575923919677734],
           [-23.54102325439453, -46.57581329345703],
           [-23.541053771972656, -46.575923919677734],
           [-23.54108428955078, -46.5760498046875],
           [-23.54111671447754, -46.5761833190918],
           [-23.541147232055664, -46.57631301879883],
           [-23.541183471679688, -46.57646560668945],
           [-23.54121208190918, -46.57659149169922],
           [-23.54124641418457, -46.57674026489258],
           [-23.541257858276367, -46.576786041259766],
           [-23.54128074645996, -46.576904296875],
           [-23.54128646850586, -46.576961517333984],
           [-23.54128074645996, -46.577003479003906],
           [-23.541263580322266, -46.57703399658203],
           [-23.541231155395508, -46.577064514160156],
           [-23.54119110107422, -46.57707977294922],
           [-23.541152954101562, -46.57708740234375],
           [-23.54113006591797, -46.57707977294922],
           [-23.541101455688477, -46.577056884765625],
           [-23.541080474853516, -46.5770378112793],
           [-23.54104995727539, -46.5768928527832],
           [-23.541027069091797, -46.576778411865234],
           [-23.541013717651367, -46.57670211791992],
           [-23.540987014770508, -46.57658386230469],
           [-23.540973663330078, -46.576515197753906],
           [-23.540950775146484, -46.5764045715332],
           [-23.540939331054688, -46.57634735107422],
           [-23.54092025756836, -46.576255798339844],
           [-23.5408992767334, -46.5761604309082],
           [-23.540876388549805, -46.5760383605957],
           [-23.540855407714844, -46.5759391784668],
           [-23.54082679748535, -46.575809478759766],
           [-23.540807723999023, -46.5756950378418],
           [-23.54079818725586, -46.575645446777344],
           [-23.54079246520996, -46.57561111450195],
           [-23.540790557861328, -46.57556915283203],
           [-23.540790557861328, -46.57553482055664],
           [-23.54082679748535, -46.57541275024414],
           [-23.541763305664062, -46.575225830078125],
           [-23.54190444946289, -46.5751838684082],
           [-23.541963577270508, -46.57533264160156],
           [-23.542055130004883, -46.57576370239258],
           [-23.542163848876953, -46.57634353637695],
           [-23.542272567749023, -46.57691955566406],
           [-23.542287826538086, -46.57706069946289],
           [-23.542236328125, -46.577091217041016],
           [-23.542224884033203, -46.577117919921875],
           [-23.542213439941406, -46.577152252197266],
           [-23.542402267456055, -46.57798767089844],
           [-23.54251480102539, -46.578487396240234],
           [-23.543312072753906, -46.57829284667969],
           [-23.543834686279297, -46.578155517578125],
           [-23.543996810913086, -46.57810974121094],
           [-23.543981552124023, -46.57821273803711],
           [-23.54397964477539, -46.57832717895508],
           [-23.543882369995117, -46.57850646972656],
           [-23.54383659362793, -46.57859802246094],
           [-23.543790817260742, -46.578670501708984],
           [-23.543720245361328, -46.57875061035156],
           [-23.543474197387695, -46.5789794921875],
           [-23.543216705322266, -46.579246520996094],
           [-23.543140411376953, -46.579376220703125],
           [-23.543115615844727, -46.57943344116211],
           [-23.5430965423584, -46.57951354980469],
           [-23.543079376220703, -46.57958984375],
           [-23.543071746826172, -46.579708099365234],
           [-23.543075561523438, -46.579872131347656],
           [-23.5430850982666, -46.58013916015625],
           [-23.543094635009766, -46.58030319213867],
           [-23.543094635009766, -46.58035659790039],
           [-23.543100357055664, -46.580509185791016],
           [-23.543107986450195, -46.58073043823242],
           [-23.54311752319336, -46.58091735839844],
           [-23.543123245239258, -46.58102798461914],
           [-23.543149948120117, -46.58126449584961],
           [-23.543170928955078, -46.581363677978516],
           [-23.543210983276367, -46.58153533935547],
           [-23.543243408203125, -46.58169174194336],
           [-23.543254852294922, -46.58182144165039],
           [-23.543214797973633, -46.58189010620117],
           [-23.54315948486328, -46.58193588256836],
           [-23.54310417175293, -46.58195114135742],
           [-23.543067932128906, -46.581947326660156],
           [-23.542999267578125, -46.58192825317383],
           [-23.542945861816406, -46.58186721801758],
           [-23.542917251586914, -46.581790924072266],
           [-23.542903900146484, -46.58169174194336],
           [-23.542888641357422, -46.58149719238281],
           [-23.542879104614258, -46.58137893676758],
           [-23.542863845825195, -46.58126449584961],
           [-23.542871475219727, -46.5811882019043],
           [-23.542877197265625, -46.581024169921875],
           [-23.542896270751953, -46.58091735839844],
           [-23.542938232421875, -46.580787658691406],
           [-23.542991638183594, -46.58073425292969],
           [-23.54305648803711, -46.58068084716797],
           [-23.543088912963867, -46.580604553222656],
           [-23.543170928955078, -46.580570220947266],
           [-23.543291091918945, -46.580535888671875],
           [-23.543445587158203, -46.58050537109375],
           [-23.544200897216797, -46.580345153808594],
           [-23.545089721679688, -46.58017349243164],
           [-23.545944213867188, -46.579994201660156],
           [-23.546371459960938, -46.57987976074219],
           [-23.54654884338379, -46.579917907714844],
           [-23.54677963256836, -46.58004379272461],
           [-23.5468692779541, -46.58010482788086],
           [-23.547679901123047, -46.5797233581543],
           [-23.54821014404297, -46.579471588134766],
           [-23.54888343811035, -46.57929611206055],
           [-23.549179077148438, -46.57921600341797],
           [-23.54966163635254, -46.57904052734375],
           [-23.54979133605957, -46.578983306884766],
           [-23.55057144165039, -46.57857131958008],
           [-23.55108642578125, -46.578304290771484],
           [-23.551271438598633, -46.5786018371582],
           [-23.551462173461914, -46.578914642333984],
           [-23.55156135559082, -46.57908248901367],
           [-23.551727294921875, -46.5793571472168],
           [-23.551740646362305, -46.579376220703125],
           [-23.55175018310547, -46.57939529418945],
           [-23.551803588867188, -46.57948684692383],
           [-23.55185890197754, -46.57957458496094],
           [-23.551536560058594, -46.57975387573242],
           [-23.551530838012695, -46.57975769042969],
           [-23.55150032043457, -46.57977294921875],
           [-23.551372528076172, -46.5798454284668],
           [-23.55132484436035, -46.579872131347656],
           [-23.550722122192383, -46.58021545410156],
           [-23.55116081237793, -46.58067321777344],
           [-23.551429748535156, -46.58094787597656],
           [-23.552165985107422, -46.58171463012695],
           [-23.552671432495117, -46.58225631713867],
           [-23.5531005859375, -46.58272933959961],
           [-23.55335235595703, -46.58300018310547],
           [-23.553691864013672, -46.5833740234375],
           [-23.55375099182129, -46.583438873291016],
           [-23.553956985473633, -46.58366775512695],
           [-23.554031372070312, -46.583717346191406],
           [-23.554126739501953, -46.58378982543945],
           [-23.554401397705078, -46.58393859863281],
           [-23.554624557495117, -46.58405685424805],
           [-23.554866790771484, -46.58418273925781],
           [-23.5554256439209, -46.58448791503906],
           [-23.555545806884766, -46.58454895019531],
           [-23.556198120117188, -46.58490753173828],
           [-23.55642318725586, -46.58502197265625],
           [-23.556734085083008, -46.58518981933594],
           [-23.55701446533203, -46.58534240722656],
           [-23.557254791259766, -46.585479736328125],
           [-23.557443618774414, -46.5855712890625],
           [-23.557790756225586, -46.58575439453125],
           [-23.557825088500977, -46.58577346801758],
           [-23.558259963989258, -46.58601379394531],
           [-23.558460235595703, -46.586116790771484],
           [-23.55872344970703, -46.58626174926758],
           [-23.558765411376953, -46.58628845214844],
           [-23.559249877929688, -46.58655548095703],
           [-23.559497833251953, -46.58668518066406],
           [-23.559728622436523, -46.58679962158203],
           [-23.55999755859375, -46.58694076538086],
           [-23.560213088989258, -46.586448669433594],
           [-23.560380935668945, -46.5860710144043],
           [-23.56039047241211, -46.5860481262207],
           [-23.56059455871582, -46.58558654785156],
           [-23.560718536376953, -46.58530807495117],
           [-23.560850143432617, -46.58500289916992],
           [-23.561260223388672, -46.58412170410156],
           [-23.5616397857666, -46.58324432373047],
           [-23.561660766601562, -46.58311080932617],
           [-23.561702728271484, -46.58271026611328],
           [-23.561752319335938, -46.581974029541016],
           [-23.561817169189453, -46.581119537353516],
           [-23.56182098388672, -46.58102035522461],
           [-23.561830520629883, -46.58094787597656],
           [-23.561840057373047, -46.58083724975586],
           [-23.561864852905273, -46.58050537109375],
           [-23.56192970275879, -46.57970428466797],
           [-23.56226921081543, -46.57883834838867],
           [-23.562644958496094, -46.57793045043945],
           [-23.562713623046875, -46.57802963256836],
           [-23.562803268432617, -46.578182220458984],
           [-23.56298828125, -46.578372955322266],
           [-23.56321907043457, -46.57855987548828],
           [-23.563396453857422, -46.57868576049805],
           [-23.563615798950195, -46.578800201416016],
           [-23.56396484375, -46.57896041870117],
           [-23.56415557861328, -46.579044342041016],
           [-23.564790725708008, -46.579349517822266],
           [-23.565147399902344, -46.57951736450195],
           [-23.565256118774414, -46.57963943481445],
           [-23.565427780151367, -46.579776763916016],
           [-23.56553840637207, -46.57985305786133],
           [-23.56561279296875, -46.57990646362305],
           [-23.565711975097656, -46.57996368408203],
           [-23.565887451171875, -46.58005142211914],
           [-23.565988540649414, -46.580074310302734],
           [-23.56610870361328, -46.5800895690918],
           [-23.566164016723633, -46.58009338378906],
           [-23.566377639770508, -46.580116271972656],
           [-23.567047119140625, -46.580177307128906],
           [-23.567455291748047, -46.58021545410156],
           [-23.567432403564453, -46.58066940307617],
           [-23.56739044189453, -46.58134078979492],
           [-23.567331314086914, -46.58207702636719],
           [-23.56730842590332, -46.58247375488281],
           [-23.567304611206055, -46.58264923095703],
           [-23.56728744506836, -46.583621978759766],
           [-23.567283630371094, -46.58464050292969],
           [-23.567276000976562, -46.58571243286133],
           [-23.567049026489258, -46.5857048034668],
           [-23.566835403442383, -46.58567428588867],
           [-23.56669044494629, -46.585662841796875],
           [-23.566450119018555, -46.58563995361328],
           [-23.566030502319336, -46.58560562133789],
           [-23.565752029418945, -46.58558654785156],
           [-23.56557846069336, -46.585567474365234],
           [-23.56502914428711, -46.585514068603516],
           [-23.564966201782227, -46.58568572998047],
           [-23.564611434936523, -46.586463928222656],
           [-23.564531326293945, -46.586639404296875],
           [-23.564401626586914, -46.58692169189453],
           [-23.564361572265625, -46.5870246887207],
           [-23.5639705657959, -46.58787536621094],
           [-23.563753128051758, -46.58834457397461],
           [-23.56354522705078, -46.58881759643555],
           [-23.563173294067383, -46.589637756347656],
           [-23.562679290771484, -46.59071350097656],
           [-23.562414169311523, -46.591312408447266],
           [-23.562305450439453, -46.59157180786133],
           [-23.56228256225586, -46.59164047241211],
           [-23.562232971191406, -46.591758728027344],
           [-23.56220817565918, -46.59185028076172],
           [-23.562196731567383, -46.59195327758789],
           [-23.56171417236328, -46.59238052368164],
           [-23.561391830444336, -46.592681884765625],
           [-23.56233787536621, -46.593257904052734],
           [-23.562416076660156, -46.593162536621094],
           [-23.562725067138672, -46.59281921386719],
           [-23.563045501708984, -46.5924072265625],
           [-23.563091278076172, -46.592342376708984],
           [-23.563201904296875, -46.5921516418457],
           [-23.56328582763672, -46.59198760986328],
           [-23.5635986328125, -46.59138870239258],
           [-23.563552856445312, -46.59136199951172],
           [-23.563457489013672, -46.59130096435547]]


mapa_linhas = folium.Map(
    location=[-23.563553, -46.591361],
    zoom_start=11,
    control_scale=True,
    # tiles="cartodbpositron"
)


for i in range(len(posicao)-1):
    folium.PolyLine(locations=[[posicao[i][0], posicao[i][1]], [posicao[i+1][0], posicao[i+1][1]]],
                    color='navy').add_to(mapa_linhas)

mapa_linhas.add_child(folium.LatLngPopup())

st_data = st_folium(mapa_linhas, width=1000)