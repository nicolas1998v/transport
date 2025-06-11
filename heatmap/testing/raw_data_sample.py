{
    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.ItineraryResult, Tfl.Api.Presentation.Entities",
    "journeys": [
        {
            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Journey, Tfl.Api.Presentation.Entities",
            "startDateTime": "2025-02-11T11:29:00",
            "duration": 53,
            "arrivalDateTime": "2025-02-11T12:22:00",
            "alternativeRoute": false,
            "legs": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 6,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to Hoop Lane, Golders Green",
                        "detailed": "Walk to Hoop Lane, Golders Green",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "Ravenscroft Avenue for 161 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Ravenscroft Avenue",
                                "distance": 161,
                                "cumulativeDistance": 161,
                                "skyDirection": 43,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 145,
                                "latitude": 51.57592562195,
                                "longitude": -0.20105195994,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Golders Green Road, continue for 162 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Golders Green Road",
                                "distance": 162,
                                "cumulativeDistance": 324,
                                "skyDirection": 42,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 291,
                                "latitude": 51.574852864979995,
                                "longitude": -0.20263847656,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 52 metres",
                                "turnDirection": "RIGHT",
                                "streetName": "",
                                "distance": 52,
                                "cumulativeDistance": 376,
                                "skyDirection": 222,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 337,
                                "latitude": 51.573971924220004,
                                "longitude": -0.20089819686,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn right",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T11:29:00",
                    "arrivalTime": "2025-02-11T11:35:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "platformName": "",
                        "icsCode": "99999997",
                        "commonName": "NW11 8AU",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57605497606,
                        "lon": -0.20127776128
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G00015322",
                        "platformName": "S",
                        "stopLetter": "S",
                        "icsCode": "1015322",
                        "individualStopId": "490015322GR",
                        "commonName": "Hoop Lane",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57364875766,
                        "lon": -0.20034814640999998
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57605497606, -0.20127776128],[51.57592562195, -0.20105195994],[51.57549498969, -0.20170395398],[51.57485286498, -0.20263847656],[51.57452970641, -0.20208840308],[51.57448366697, -0.20201806327],[51.57445560132, -0.20194701431],[51.57433523544, -0.20172086417],[51.57426112991, -0.20157947660],[51.57398378542, -0.20108533336],[51.57391910826, -0.20097243786],[51.57397192422, -0.20089819686],[51.57367616075, -0.20037592618],[51.57365752339, -0.20033336915]]",
                        "stopPoints": [],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "100",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "distance": 376.0,
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:31:00",
                    "scheduledArrivalTime": "2025-02-11T11:37:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 2,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "240 bus to Golders Green Station",
                        "detailed": "240 bus towards Golders Green Station",
                        "steps": []
                    },
                    "obstacles": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000087,
                            "position": "AFTER"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000087,
                            "position": "AFTER"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000087,
                            "position": "AFTER"
                        }
                    ],
                    "departureTime": "2025-02-11T11:34:00",
                    "arrivalTime": "2025-02-11T11:36:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G00015322",
                        "platformName": "S",
                        "stopLetter": "S",
                        "icsCode": "1015322",
                        "individualStopId": "490015322GR",
                        "commonName": "Hoop Lane",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57364875766,
                        "lon": -0.20034814640999998
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUGGN",
                        "platformName": "",
                        "stopLetter": "GI",
                        "icsCode": "1000087",
                        "individualStopId": "490000087GI",
                        "commonName": "Golders Green Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.571993320759994,
                        "lon": -0.19443929263
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57361864256, -0.20040836998],[51.57343127816, -0.20009899886],[51.57324360890, -0.19980596048],[51.57316621832, -0.19968505667],[51.57308860806, -0.19956156440],[51.57293293117, -0.19931416622],[51.57283177402, -0.19915639468],[51.57276160597, -0.19902568329],[51.57268309678, -0.19886124546],[51.57254325579, -0.19847396964],[51.57249750428, -0.19832295761],[51.57247363500, -0.19824424409],[51.57226760053, -0.19754615707],[51.57215376312, -0.19714848005],[51.57213737232, -0.19708330246],[51.57213737232, -0.19708330246],[51.57210252351, -0.19694472763],[51.57209285066, -0.19690629220],[51.57206691318, -0.19678667921],[51.57203125331, -0.19659616429],[51.57199611503, -0.19644545726],[51.57194097731, -0.19619294121],[51.57192537046, -0.19609023665],[51.57192183879, -0.19593654736],[51.57187181099, -0.19561874853],[51.57185897289, -0.19552069672],[51.57180548565, -0.19520606617],[51.57183856994, -0.19515295043],[51.57189236974, -0.19506106191],[51.57190479395, -0.19503863544],[51.57194495469, -0.19494281346],[51.57198359528, -0.19486508968],[51.57200679943, -0.19479519255],[51.57202769905, -0.19475670091],[51.57206567715, -0.19467683849],[51.57208046678, -0.19462112785],[51.57205569749, -0.19450161418],[51.57204243167, -0.19443744290]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "490G00006838",
                                "name": "Finchley Road",
                                "uri": "/StopPoint/490G00006838",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUGGN",
                                "name": "Golders Green Underground Station",
                                "uri": "/StopPoint/940GZZLUGGN",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "240",
                            "directions": [
                                "Golders Green Station"
                            ],
                            "lineIdentifier": {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "240",
                                "name": "240",
                                "uri": "/Line/240",
                                "type": "Line",
                                "crowding": {
                                    "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
                                },
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            "direction": "Inbound"
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "bus",
                        "name": "bus",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "3",
                        "network": "tfl"
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:37:00",
                    "scheduledArrivalTime": "2025-02-11T11:40:00",
                    "interChangeDuration": "4",
                    "interChangePosition": "AFTER"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 25,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Northern line to Borough",
                        "detailed": "Northern line towards Morden via Bank",
                        "steps": []
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T11:42:00",
                    "arrivalTime": "2025-02-11T12:07:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUGGN",
                        "platformName": "",
                        "icsCode": "1000087",
                        "individualStopId": "9400ZZLUGGN2",
                        "commonName": "Golders Green Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57242047478,
                        "lon": -0.1941481846
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUBOR",
                        "platformName": "",
                        "icsCode": "1000026",
                        "individualStopId": "9400ZZLUBOR2",
                        "commonName": "Borough Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.5009225342,
                        "lon": -0.09362625743
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57244721319, -0.19411807483],[51.57243097918, -0.19405945266],[51.57238106907, -0.19387816152],[51.57221672562, -0.19327887911],[51.57209026276, -0.19268127327],[51.57197369951, -0.19204936620],[51.57189356230, -0.19161068395],[51.57183410377, -0.19127104128],[51.57176615517, -0.19088238438],[51.57163553036, -0.19024310797],[51.57151008380, -0.18961329780],[51.57140845156, -0.18913420754],[51.57131209473, -0.18887468340],[51.57125235373, -0.18868037283],[51.57112867500, -0.18817142739],[51.57108816868, -0.18794749316],[51.57092126580, -0.18727764246],[51.57069597614, -0.18648414503],[51.57050600020, -0.18583470445],[51.57022767638, -0.18500249657],[51.56996618128, -0.18434004526],[51.56962746305, -0.18359208039],[51.56939005344, -0.18312088920],[51.56915820346, -0.18271268299],[51.56894742554, -0.18241099649],[51.56864321431, -0.18196989928],[51.56842355504, -0.18172773449],[51.56822308289, -0.18155738602],[51.56800770788, -0.18141764662],[51.56534518889, -0.18013817553],[51.56473311550, -0.17989136293],[51.56397765176, -0.17965865156],[51.56319407879, -0.17949791058],[51.56237043060, -0.17937974956],[51.56152518247, -0.17932997461],[51.56018830767, -0.17936634408],[51.55909850573, -0.17945242483],[51.55879112089, -0.17952038564],[51.55847528177, -0.17965201438],[51.55816049343, -0.17975864201],[51.55795358378, -0.17975319825],[51.55774838565, -0.17968998203],[51.55750530400, -0.17955557214],[51.55734565503, -0.17943168086],[51.55712655761, -0.17921452115],[51.55700556375, -0.17886390143],[51.55670459950, -0.17843016867],[51.55661549441, -0.17829178000],[51.55654375823, -0.17817394577],[51.55654375823, -0.17817394577],[51.55651389686, -0.17812489549],[51.55642738257, -0.17797385414],[51.55633487726, -0.17780184718],[51.55627866619, -0.17769128574],[51.55601358095, -0.17741409223],[51.55587465053, -0.17692802660],[51.55560045243, -0.17601836367],[51.55542790008, -0.17536559710],[51.55518137958, -0.17431679460],[51.55481941309, -0.17287117733],[51.55447671606, -0.17189001668],[51.55364712826, -0.17002440230],[51.55324920156, -0.16925697052],[51.55300527015, -0.16878657075],[51.55236280262, -0.16764875890],[51.55170850454, -0.16662353005],[51.55131407582, -0.16598352753],[51.55077217389, -0.16510815798],[51.55052275471, -0.16478240827],[51.55040627441, -0.16462482746],[51.55040627441, -0.16462482746],[51.55036869131, -0.16457398326],[51.55022370262, -0.16437658907],[51.55001910537, -0.16408798646],[51.54956178063, -0.16345214854],[51.54891531397, -0.16218297251],[51.54864556333, -0.16171946432],[51.54759897948, -0.16011037598],[51.54718631418, -0.15927896703],[51.54667930218, -0.15802303202],[51.54641562700, -0.15731760424],[51.54619185577, -0.15679416916],[51.54599566191, -0.15640634833],[51.54568082315, -0.15584477991],[51.54442977517, -0.15388812616],[51.54422637948, -0.15351510984],[51.54422637948, -0.15351510984],[51.54420180134, -0.15347003528],[51.54369297002, -0.15220537760],[51.54349069904, -0.15156979241],[51.54331082088, -0.15088888677],[51.54294143462, -0.14900859983],[51.54270180102, -0.14787572172],[51.54244552083, -0.14709584285],[51.54216140464, -0.14643838580],[51.54186006810, -0.14585230007],[51.54141259721, -0.14517496657],[51.54086287055, -0.14440619581],[51.54049393438, -0.14396435689],[51.53997926607, -0.14347942596],[51.53954625749, -0.14307467555],[51.53930268349, -0.14284662026],[51.53930268349, -0.14284662026],[51.53927069065, -0.14281666598],[51.53905908868, -0.14262296484],[51.53893021736, -0.14252582854],[51.53886735645, -0.14248584855],[51.53879171847, -0.14244537950],[51.53870802723, -0.14241879337],[51.53859611696, -0.14239898016],[51.53849036131, -0.14236464063],[51.53840296759, -0.14232003639],[51.53820816190, -0.14214786382],[51.53794492086, -0.14193579706],[51.53565239526, -0.13947437898],[51.53537316812, -0.13920156595],[51.53519240948, -0.13906489224],[51.53505367242, -0.13900927025],[51.53493846154, -0.13897417316],[51.53478422038, -0.13894456129],[51.53460498658, -0.13893802976],[51.53431951470, -0.13896885026],[51.53274536282, -0.13909807761],[51.53249656747, -0.13907708062],[51.53227866411, -0.13904775914],[51.53160630670, -0.13887837504],[51.53133158807, -0.13880480284],[51.53066350707, -0.13854225788],[51.52910641137, -0.13766116456],[51.52881471333, -0.13743576478],[51.52860402957, -0.13723820158],[51.52839555351, -0.13695318408],[51.52831007490, -0.13682548058],[51.52817409072, -0.13649036405],[51.52808567570, -0.13596848429],[51.52805895714, -0.13542462336],[51.52808747311, -0.13503492733],[51.52814121354, -0.13465948158],[51.52821373973, -0.13430618962],[51.52832803101, -0.13388198814],[51.52844536426, -0.13354733290],[51.52857701044, -0.13318541921],[51.52867954339, -0.13284602474],[51.52867954339, -0.13284602474],[51.52878749531, -0.13248868775],[51.52904617283, -0.13167319890],[51.52930150690, -0.13099249358],[51.52942771444, -0.13070172077],[51.52974516015, -0.12999149879],[51.52994849405, -0.12954113135],[51.53009160341, -0.12916574829],[51.53023389676, -0.12871110046],[51.53038863577, -0.12819682764],[51.53049273202, -0.12760288180],[51.53056540604, -0.12694476728],[51.53068154954, -0.12511286130],[51.53070958327, -0.12438578422],[51.53071132082, -0.12434260422],[51.53074378487, -0.12345992227],[51.53078510403, -0.12236681006],[51.53081618083, -0.12189158503],[51.53081618083, -0.12189158503],[51.53093541846, -0.12006792881],[51.53100106842, -0.11907530603],[51.53103706738, -0.11859486631],[51.53142181793, -0.11363138281],[51.53185438856, -0.10927095264],[51.53189210019, -0.10790660194],[51.53188982863, -0.10721953481],[51.53185132750, -0.10654449612],[51.53182152646, -0.10613006264],[51.53178477233, -0.10592355228],[51.53178477233, -0.10592355228],[51.53174072716, -0.10567607887],[51.53165407080, -0.10532167933],[51.53148756826, -0.10472289803],[51.53146990265, -0.10465918391],[51.52969716785, -0.09776261920],[51.52803729977, -0.09117917490],[51.52737091322, -0.08872479725],[51.52701922855, -0.08821245835],[51.52669706845, -0.08795579012],[51.52563668314, -0.08754307967],[51.52544559343, -0.08752875534],[51.52544559343, -0.08752875534],[51.52540970351, -0.08752606500],[51.52532137769, -0.08751938649],[51.52433377897, -0.08744544211],[51.52221487570, -0.08700504876],[51.52169258763, -0.08700502605],[51.52066236948, -0.08716855937],[51.51978142139, -0.08724900299],[51.51951442056, -0.08732548594],[51.51914857395, -0.08748913373],[51.51889769361, -0.08764808021],[51.51889769361, -0.08764808021],[51.51851200143, -0.08789243364],[51.51717937091, -0.08862481005],[51.51537349666, -0.08936512761],[51.51456442597, -0.08967368642],[51.51427286705, -0.08963933236],[51.51353521749, -0.08921491170],[51.51339225443, -0.08913326815],[51.51299595893, -0.08887429376],[51.51221178423, -0.08831072740],[51.51221178423, -0.08831072740],[51.51212635399, -0.08824933212],[51.51197490678, -0.08815479041],[51.51126843560, -0.08772363204],[51.51090988012, -0.08746310081],[51.51075254093, -0.08731058904],[51.51050709858, -0.08718713253],[51.50990281817, -0.08714427888],[51.50936685165, -0.08709409733],[51.50926563508, -0.08708551128],[51.50911569861, -0.08705057664],[51.50873036377, -0.08686294970],[51.50858929271, -0.08680919912],[51.50844337598, -0.08677813243],[51.50827771724, -0.08677167041],[51.50714208815, -0.08711061733],[51.50695377610, -0.08719286075],[51.50676428781, -0.08732429113],[51.50661277410, -0.08749591933],[51.50605242981, -0.08823396783],[51.50585241228, -0.08849739332],[51.50555221575, -0.08890982552],[51.50555221575, -0.08890982552],[51.50438862725, -0.09050837831],[51.50407139949, -0.09095766310],[51.50381428966, -0.09121105881],[51.50327927507, -0.09163369727],[51.50309747997, -0.09177399848],[51.50270149745, -0.09204240618],[51.50198272838, -0.09245194910],[51.50176227660, -0.09262065683],[51.50129931089, -0.09314427972],[51.50109358975, -0.09340602052],[51.50093647439, -0.09364805248]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUHTD",
                                "name": "Hampstead Underground Station",
                                "uri": "/StopPoint/940GZZLUHTD",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBZP",
                                "name": "Belsize Park Underground Station",
                                "uri": "/StopPoint/940GZZLUBZP",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCFM",
                                "name": "Chalk Farm Underground Station",
                                "uri": "/StopPoint/940GZZLUCFM",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCTN",
                                "name": "Camden Town Underground Station",
                                "uri": "/StopPoint/940GZZLUCTN",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUEUS",
                                "name": "Euston Underground Station",
                                "uri": "/StopPoint/940GZZLUEUS",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUKSX",
                                "name": "King's Cross St. Pancras Underground Station",
                                "uri": "/StopPoint/940GZZLUKSX",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUAGL",
                                "name": "Angel Underground Station",
                                "uri": "/StopPoint/940GZZLUAGL",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUODS",
                                "name": "Old Street Underground Station",
                                "uri": "/StopPoint/940GZZLUODS",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUMGT",
                                "name": "Moorgate Underground Station",
                                "uri": "/StopPoint/940GZZLUMGT",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBNK",
                                "name": "Bank Underground Station",
                                "uri": "/StopPoint/940GZZLUBNK",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLULNB",
                                "name": "London Bridge Underground Station",
                                "uri": "/StopPoint/940GZZLULNB",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBOR",
                                "name": "Borough Underground Station",
                                "uri": "/StopPoint/940GZZLUBOR",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "Northern",
                            "directions": [
                                "Morden via Bank"
                            ],
                            "lineIdentifier": {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "northern",
                                "name": "Northern",
                                "uri": "/Line/northern",
                                "type": "Line",
                                "crowding": {
                                    "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
                                },
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            "direction": "Inbound"
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "tube",
                        "name": "tube",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "1",
                        "network": "tfl"
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:42:00",
                    "scheduledArrivalTime": "2025-02-11T12:07:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 15,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to SE1 0RB",
                        "detailed": "Walk to SE1 0RB",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "Borough High Street for 3 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Borough High Street",
                                "distance": 3,
                                "cumulativeDistance": 3,
                                "skyDirection": 225,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 2,
                                "latitude": 51.50094050716,
                                "longitude": -0.0936255074,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Borough High Street, continue for 13 metres",
                                "turnDirection": "SLIGHT_LEFT",
                                "streetName": "Borough High Street",
                                "distance": 13,
                                "cumulativeDistance": 16,
                                "skyDirection": 225,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 14,
                                "latitude": 51.50095824607,
                                "longitude": -0.09361035890000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Take a slight left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Borough High Street, continue for 193 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Borough High Street",
                                "distance": 193,
                                "cumulativeDistance": 209,
                                "skyDirection": 22,
                                "skyDirectionDescription": "North",
                                "cumulativeTravelTime": 187,
                                "latitude": 51.501064913520004,
                                "longitude": -0.09353386611,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Great Suffolk Street, continue for 260 metres",
                                "turnDirection": "RIGHT",
                                "streetName": "Great Suffolk Street",
                                "distance": 260,
                                "cumulativeDistance": 469,
                                "skyDirection": 47,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 421,
                                "latitude": 51.49990199473,
                                "longitude": -0.09557068825000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn right",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Webber Street/Rushworth Street, continue for 209 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Webber Street/Rushworth Street",
                                "distance": 209,
                                "cumulativeDistance": 679,
                                "skyDirection": 38,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 609,
                                "latitude": 51.501007847400004,
                                "longitude": -0.09888171012000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Rushworth Street, continue for 28 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Rushworth Street",
                                "distance": 28,
                                "cumulativeDistance": 707,
                                "skyDirection": 143,
                                "skyDirectionDescription": "SouthEast",
                                "cumulativeTravelTime": 634,
                                "latitude": 51.50099684624,
                                "longitude": -0.10153328478,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        }
                    ],
                    "departureTime": "2025-02-11T12:07:00",
                    "arrivalTime": "2025-02-11T12:22:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUBOR",
                        "platformName": "",
                        "icsCode": "1000026",
                        "individualStopId": "9400ZZLUBOR2",
                        "commonName": "Borough Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.5009225342,
                        "lon": -0.09362625743
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.Place, Tfl.Api.Presentation.Entities",
                        "commonName": "SE1 0RB",
                        "placeType": "StopPoint",
                        "lat": 51.501251032750005,
                        "lon": -0.10168121278
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.50093900055, -0.09363138955],[51.50096136866, -0.09360444009],[51.50106202502, -0.09353257487],[51.50106849539, -0.09352908749],[51.50106491352, -0.09353386611],[51.50095824607, -0.09361035890],[51.50082672548, -0.09381756225],[51.50075647180, -0.09392135095],[51.50069543852, -0.09403916280],[51.50059064262, -0.09423084069],[51.50038175165, -0.09465738874],[51.50017285908, -0.09508393291],[51.50000679289, -0.09537901631],[51.49998053492, -0.09542333483],[51.49996326343, -0.09546727866],[51.49994599192, -0.09551122246],[51.49990199473, -0.09557068825],[51.49996747205, -0.09572644590],[51.49998661400, -0.09579768766],[51.50001497618, -0.09588295312],[51.50006224634, -0.09602506245],[51.50010928259, -0.09615277386],[51.50017522660, -0.09633732956],[51.50030898312, -0.09682162898],[51.50037609428, -0.09707817809],[51.50041367566, -0.09717746911],[51.50044250407, -0.09729153292],[51.50049922622, -0.09746206755],[51.50050891347, -0.09750488839],[51.50059516388, -0.09783268325],[51.50079228681, -0.09834316992],[51.50081119372, -0.09840001562],[51.50083932058, -0.09847088579],[51.50084900746, -0.09851370718],[51.50088635420, -0.09859860194],[51.50093315426, -0.09871191983],[51.50096104751, -0.09876839187],[51.50098018763, -0.09883963649],[51.50100784740, -0.09888171012],[51.50098158811, -0.09892602765],[51.50092860266, -0.09898586554],[51.50092008295, -0.09901503652],[51.50090257671, -0.09904458143],[51.50089475714, -0.09911694789],[51.50087013135, -0.09926205464],[51.50086207829, -0.09932002252],[51.50080407283, -0.09962500777],[51.50078061289, -0.09984210633],[51.50074746623, -0.10001638304],[51.50069961161, -0.10039298524],[51.50070031128, -0.10043618060],[51.50069412328, -0.10060933567],[51.50069738790, -0.10081091401],[51.50070018586, -0.10098369548],[51.50071197010, -0.10115610344],[51.50072258850, -0.10125651916],[51.50074079467, -0.10127017061],[51.50075876771, -0.10126942359],[51.50076775423, -0.10126905008],[51.50078596039, -0.10128270155],[51.50099684624, -0.10153328478],[51.50118975853, -0.10178461714],[51.50125103275, -0.10168121278]]",
                        "stopPoints": [],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "100",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "distance": 691.0,
                    "isDisrupted": false,
                    "hasFixedLocations": false,
                    "scheduledDepartureTime": "2025-02-11T12:07:00",
                    "scheduledArrivalTime": "2025-02-11T12:22:00",
                    "interChangeDuration": "5",
                    "interChangePosition": "BEFORE"
                }
            ]
        },
        {
            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Journey, Tfl.Api.Presentation.Entities",
            "startDateTime": "2025-02-11T11:32:00",
            "duration": 53,
            "arrivalDateTime": "2025-02-11T12:25:00",
            "alternativeRoute": false,
            "legs": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 6,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to Hoop Lane",
                        "detailed": "Walk to Hoop Lane",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "Ravenscroft Avenue for 311 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Ravenscroft Avenue",
                                "distance": 311,
                                "cumulativeDistance": 311,
                                "skyDirection": 222,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 279,
                                "latitude": 51.57592562195,
                                "longitude": -0.20105195994,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Finchley Road, continue for 45 metres",
                                "turnDirection": "RIGHT",
                                "streetName": "Finchley Road",
                                "distance": 45,
                                "cumulativeDistance": 356,
                                "skyDirection": 251,
                                "skyDirectionDescription": "West",
                                "cumulativeTravelTime": 321,
                                "latitude": 51.57706988292,
                                "longitude": -0.19709567344,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn right",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T11:32:00",
                    "arrivalTime": "2025-02-11T11:38:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "platformName": "",
                        "icsCode": "99999997",
                        "commonName": "NW11 8AU",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57605497606,
                        "lon": -0.20127776128
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G00008343",
                        "platformName": "",
                        "stopLetter": "->S",
                        "icsCode": "1008343",
                        "individualStopId": "490008343S",
                        "commonName": "Hoop Lane",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57667967943,
                        "lon": -0.19686577049
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57605497606, -0.20127776128],[51.57592562195, -0.20105195994],[51.57604878540, -0.20087391541],[51.57633827663, -0.20040066350],[51.57666039473, -0.19970963656],[51.57686381758, -0.19831612089],[51.57701928518, -0.19731415735],[51.57706988292, -0.19709567344],[51.57666259210, -0.19692417475]]",
                        "stopPoints": [],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "100",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "distance": 356.0,
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:32:00",
                    "scheduledArrivalTime": "2025-02-11T11:38:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 2,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "13 bus to Golders Green Station",
                        "detailed": "13 bus towards Victoria Station",
                        "steps": []
                    },
                    "obstacles": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000087,
                            "position": "AFTER"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000087,
                            "position": "AFTER"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000087,
                            "position": "AFTER"
                        }
                    ],
                    "departureTime": "2025-02-11T11:38:00",
                    "arrivalTime": "2025-02-11T11:40:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G00008343",
                        "platformName": "",
                        "stopLetter": "->S",
                        "icsCode": "1008343",
                        "individualStopId": "490008343S",
                        "commonName": "Hoop Lane",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57667967943,
                        "lon": -0.19686577049
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUGGN",
                        "platformName": "",
                        "stopLetter": "GV",
                        "icsCode": "1000087",
                        "individualStopId": "490015496GV",
                        "commonName": "Golders Green Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57295602094,
                        "lon": -0.19564219707
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57667069044, -0.19694031892],[51.57614435127, -0.19672445433],[51.57610082291, -0.19670654987],[51.57604295342, -0.19667997671],[51.57560222089, -0.19650331485],[51.57549265153, -0.19645959463],[51.57456475539, -0.19611605794],[51.57423592889, -0.19601232751],[51.57325789703, -0.19575348320],[51.57316692778, -0.19573226412],[51.57308321118, -0.19572071523],[51.57300888647, -0.19570590831],[51.57295489566, -0.19569548462]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUGGN",
                                "name": "Golders Green Underground Station",
                                "uri": "/StopPoint/940GZZLUGGN",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "13",
                            "directions": [
                                "Victoria Station"
                            ],
                            "lineIdentifier": {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "13",
                                "name": "13",
                                "uri": "/Line/13",
                                "type": "Line",
                                "crowding": {
                                    "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
                                },
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            "direction": "Outbound"
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "bus",
                        "name": "bus",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "3",
                        "network": "tfl"
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:38:00",
                    "scheduledArrivalTime": "2025-02-11T11:40:00",
                    "interChangeDuration": "4",
                    "interChangePosition": "AFTER"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 21,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Northern line to Waterloo",
                        "detailed": "Northern line towards Kennington Station via Charing Cross",
                        "steps": []
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T11:45:00",
                    "arrivalTime": "2025-02-11T12:06:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUGGN",
                        "platformName": "",
                        "icsCode": "1000087",
                        "individualStopId": "9400ZZLUGGN2",
                        "commonName": "Golders Green Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57242047478,
                        "lon": -0.1941481846
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUWLO",
                        "platformName": "",
                        "icsCode": "1000254",
                        "individualStopId": "9400ZZLUWLO7",
                        "commonName": "Waterloo Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.502858702770006,
                        "lon": -0.11381867113000001
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57244721319, -0.19411807483],[51.57243097918, -0.19405945266],[51.57238106907, -0.19387816152],[51.57221672562, -0.19327887911],[51.57209026276, -0.19268127327],[51.57197369951, -0.19204936620],[51.57189356230, -0.19161068395],[51.57183410377, -0.19127104128],[51.57176615517, -0.19088238438],[51.57163553036, -0.19024310797],[51.57151008380, -0.18961329780],[51.57140845156, -0.18913420754],[51.57131209473, -0.18887468340],[51.57125235373, -0.18868037283],[51.57112867500, -0.18817142739],[51.57108816868, -0.18794749316],[51.57092126580, -0.18727764246],[51.57069597614, -0.18648414503],[51.57050600020, -0.18583470445],[51.57022767638, -0.18500249657],[51.56996618128, -0.18434004526],[51.56962746305, -0.18359208039],[51.56939005344, -0.18312088920],[51.56915820346, -0.18271268299],[51.56894742554, -0.18241099649],[51.56864321431, -0.18196989928],[51.56842355504, -0.18172773449],[51.56822308289, -0.18155738602],[51.56800770788, -0.18141764662],[51.56534518889, -0.18013817553],[51.56473311550, -0.17989136293],[51.56397765176, -0.17965865156],[51.56319407879, -0.17949791058],[51.56237043060, -0.17937974956],[51.56152518247, -0.17932997461],[51.56018830767, -0.17936634408],[51.55909850573, -0.17945242483],[51.55879112089, -0.17952038564],[51.55847528177, -0.17965201438],[51.55816049343, -0.17975864201],[51.55795358378, -0.17975319825],[51.55774838565, -0.17968998203],[51.55750530400, -0.17955557214],[51.55734565503, -0.17943168086],[51.55712655761, -0.17921452115],[51.55700556375, -0.17886390143],[51.55670459950, -0.17843016867],[51.55661549441, -0.17829178000],[51.55654375823, -0.17817394577],[51.55654375823, -0.17817394577],[51.55651389686, -0.17812489549],[51.55642738257, -0.17797385414],[51.55633487726, -0.17780184718],[51.55627866619, -0.17769128574],[51.55601358095, -0.17741409223],[51.55587465053, -0.17692802660],[51.55560045243, -0.17601836367],[51.55542790008, -0.17536559710],[51.55518137958, -0.17431679460],[51.55481941309, -0.17287117733],[51.55447671606, -0.17189001668],[51.55364712826, -0.17002440230],[51.55324920156, -0.16925697052],[51.55300527015, -0.16878657075],[51.55236280262, -0.16764875890],[51.55170850454, -0.16662353005],[51.55131407582, -0.16598352753],[51.55077217389, -0.16510815798],[51.55052275471, -0.16478240827],[51.55040627441, -0.16462482746],[51.55040627441, -0.16462482746],[51.55036869131, -0.16457398326],[51.55022370262, -0.16437658907],[51.55001910537, -0.16408798646],[51.54956178063, -0.16345214854],[51.54891531397, -0.16218297251],[51.54864556333, -0.16171946432],[51.54759897948, -0.16011037598],[51.54718631418, -0.15927896703],[51.54667930218, -0.15802303202],[51.54641562700, -0.15731760424],[51.54619185577, -0.15679416916],[51.54599566191, -0.15640634833],[51.54568082315, -0.15584477991],[51.54442977517, -0.15388812616],[51.54422637948, -0.15351510984],[51.54422637948, -0.15351510984],[51.54420180134, -0.15347003528],[51.54369297002, -0.15220537760],[51.54349069904, -0.15156979241],[51.54331082088, -0.15088888677],[51.54294143462, -0.14900859983],[51.54270180102, -0.14787572172],[51.54244552083, -0.14709584285],[51.54216140464, -0.14643838580],[51.54186006810, -0.14585230007],[51.54141259721, -0.14517496657],[51.54086287055, -0.14440619581],[51.54049393438, -0.14396435689],[51.53997926607, -0.14347942596],[51.53954625749, -0.14307467555],[51.53930268349, -0.14284662026],[51.53930268349, -0.14284662026],[51.53927069065, -0.14281666598],[51.53905908868, -0.14262296484],[51.53893021736, -0.14252582854],[51.53886610569, -0.14249772398],[51.53879215482, -0.14248429602],[51.53872712587, -0.14247209105],[51.53865413335, -0.14244535769],[51.53852446906, -0.14234926441],[51.53830389767, -0.14212868006],[51.53804388294, -0.14189888934],[51.53759793325, -0.14152339299],[51.53722208594, -0.14115687176],[51.53587472152, -0.13966920036],[51.53536240831, -0.13917518538],[51.53443261754, -0.13837234812],[51.53439826999, -0.13833594918],[51.53439826999, -0.13833594918],[51.53140359630, -0.13516267410],[51.53029117489, -0.13405113360],[51.52996109811, -0.13381607504],[51.52973182336, -0.13371645628],[51.52949211660, -0.13367897067],[51.52904089163, -0.13370838043],[51.52876497315, -0.13372917898],[51.52853541226, -0.13382636522],[51.52827841643, -0.13400785713],[51.52812489847, -0.13421249339],[51.52812489847, -0.13421249339],[51.52810045153, -0.13424508047],[51.52787613634, -0.13465517822],[51.52764335524, -0.13519464634],[51.52676499316, -0.13743752851],[51.52662629192, -0.13779768480],[51.52656102371, -0.13795171840],[51.52649495743, -0.13807248262],[51.52637265618, -0.13822523777],[51.52623543463, -0.13832180105],[51.52606678261, -0.13836443204],[51.52586635969, -0.13834867618],[51.52568049934, -0.13829859309],[51.52460572114, -0.13774937140],[51.52433416050, -0.13761989917],[51.52430969175, -0.13760340144],[51.52430969175, -0.13760340144],[51.52371341728, -0.13720137737],[51.52293956374, -0.13650758935],[51.52067909654, -0.13435148445],[51.52067909654, -0.13435148445],[51.52055245915, -0.13423070105],[51.51864016394, -0.13222808327],[51.51706806734, -0.13077006840],[51.51613105274, -0.13025698959],[51.51596857321, -0.13018181068],[51.51596857321, -0.13018181068],[51.51568605801, -0.13005109282],[51.51523949615, -0.12984281399],[51.51422858201, -0.12956239027],[51.51350429258, -0.12922772006],[51.51332429749, -0.12912844494],[51.51312930027, -0.12900759075],[51.51261218726, -0.12868923516],[51.51225059421, -0.12844665936],[51.51213905806, -0.12840540140],[51.51203115308, -0.12837192122],[51.51200497920, -0.12836593227],[51.51196959664, -0.12835966944],[51.51196959664, -0.12835966944],[51.51190713396, -0.12834861335],[51.51177560511, -0.12832806336],[51.51151139961, -0.12829392827],[51.51058659975, -0.12833846125],[51.51041588474, -0.12831360925],[51.51027052219, -0.12826581344],[51.51017063642, -0.12822206252],[51.50997660635, -0.12809426326],[51.50980826317, -0.12793068166],[51.50968077013, -0.12775735643],[51.50956083679, -0.12752809616],[51.50934906048, -0.12698167397],[51.50910259868, -0.12621749217],[51.50902516676, -0.12599197084],[51.50882305561, -0.12559803992],[51.50882305561, -0.12559803992],[51.50850112383, -0.12497058140],[51.50833539100, -0.12467245912],[51.50826281099, -0.12447498943],[51.50818219162, -0.12420219559],[51.50808179489, -0.12372746027],[51.50800153559, -0.12334801696],[51.50794653251, -0.12310832653],[51.50777056295, -0.12260917870],[51.50766457085, -0.12229930905],[51.50766457085, -0.12229930905],[51.50752169097, -0.12188160337],[51.50733165808, -0.12125709807],[51.50711461772, -0.12051309638],[51.50694955166, -0.11998239282],[51.50665668321, -0.11915348065],[51.50640692844, -0.11859644712],[51.50617561461, -0.11809601095],[51.50591010917, -0.11743199716],[51.50559953546, -0.11680644975],[51.50523070874, -0.11613749093],[51.50500619435, -0.11575308380],[51.50475193619, -0.11538129106],[51.50442633224, -0.11500740343],[51.50419516030, -0.11479086257],[51.50395149472, -0.11458031503],[51.50357063784, -0.11431044830],[51.50285519622, -0.11383258432]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUHTD",
                                "name": "Hampstead Underground Station",
                                "uri": "/StopPoint/940GZZLUHTD",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBZP",
                                "name": "Belsize Park Underground Station",
                                "uri": "/StopPoint/940GZZLUBZP",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCFM",
                                "name": "Chalk Farm Underground Station",
                                "uri": "/StopPoint/940GZZLUCFM",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCTN",
                                "name": "Camden Town Underground Station",
                                "uri": "/StopPoint/940GZZLUCTN",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUMTC",
                                "name": "Mornington Crescent Underground Station",
                                "uri": "/StopPoint/940GZZLUMTC",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUEUS",
                                "name": "Euston Underground Station",
                                "uri": "/StopPoint/940GZZLUEUS",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUWRR",
                                "name": "Warren Street Underground Station",
                                "uri": "/StopPoint/940GZZLUWRR",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUGDG",
                                "name": "Goodge Street Underground Station",
                                "uri": "/StopPoint/940GZZLUGDG",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUTCR",
                                "name": "Tottenham Court Road Underground Station",
                                "uri": "/StopPoint/940GZZLUTCR",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLULSQ",
                                "name": "Leicester Square Underground Station",
                                "uri": "/StopPoint/940GZZLULSQ",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCHX",
                                "name": "Charing Cross Underground Station",
                                "uri": "/StopPoint/940GZZLUCHX",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUEMB",
                                "name": "Embankment Underground Station",
                                "uri": "/StopPoint/940GZZLUEMB",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUWLO",
                                "name": "Waterloo Underground Station",
                                "uri": "/StopPoint/940GZZLUWLO",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "Northern",
                            "directions": [
                                "Kennington Station via Charing Cross"
                            ],
                            "lineIdentifier": {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "northern",
                                "name": "Northern",
                                "uri": "/Line/northern",
                                "type": "Line",
                                "crowding": {
                                    "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
                                },
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            "direction": "Inbound"
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "tube",
                        "name": "tube",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "1",
                        "network": "tfl"
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:45:00",
                    "scheduledArrivalTime": "2025-02-11T12:06:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 7,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to Waterloo Station / Waterloo Road",
                        "detailed": "Walk to Waterloo Station / Waterloo Road",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": " for 107 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "",
                                "distance": 107,
                                "cumulativeDistance": 107,
                                "skyDirection": 217,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 96,
                                "latitude": 51.5028771391,
                                "longitude": -0.11384672749000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 16 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "",
                                "distance": 16,
                                "cumulativeDistance": 123,
                                "skyDirection": 199,
                                "skyDirectionDescription": "South",
                                "cumulativeTravelTime": 111,
                                "latitude": 51.50358819077,
                                "longitude": -0.11332745969000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 46 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "",
                                "distance": 46,
                                "cumulativeDistance": 170,
                                "skyDirection": 191,
                                "skyDirectionDescription": "South",
                                "cumulativeTravelTime": 153,
                                "latitude": 51.50373151275,
                                "longitude": -0.11329272182000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 44 metres",
                                "turnDirection": "RIGHT",
                                "streetName": "",
                                "distance": 44,
                                "cumulativeDistance": 215,
                                "skyDirection": 204,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 193,
                                "latitude": 51.50411353389,
                                "longitude": -0.11300316767,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn right",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Waterloo Road, continue for 27 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Waterloo Road",
                                "distance": 27,
                                "cumulativeDistance": 242,
                                "skyDirection": 290,
                                "skyDirectionDescription": "West",
                                "cumulativeTravelTime": 217,
                                "latitude": 51.50402315399,
                                "longitude": -0.11241612517,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 2 metres",
                                "turnDirection": "LEFT",
                                "streetName": "",
                                "distance": 2,
                                "cumulativeDistance": 245,
                                "skyDirection": 318,
                                "skyDirectionDescription": "NorthWest",
                                "cumulativeTravelTime": 239,
                                "latitude": 51.50392749369,
                                "longitude": -0.11205984957000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Waterloo Road, continue for 64 metres",
                                "turnDirection": "SLIGHT_RIGHT",
                                "streetName": "Waterloo Road",
                                "distance": 64,
                                "cumulativeDistance": 309,
                                "skyDirection": 305,
                                "skyDirectionDescription": "NorthWest",
                                "cumulativeTravelTime": 297,
                                "latitude": 51.50394477142,
                                "longitude": -0.11201590799000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Take a slight right",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T12:06:00",
                    "arrivalTime": "2025-02-11T12:13:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUWLO",
                        "platformName": "",
                        "icsCode": "1000254",
                        "individualStopId": "9400ZZLUWLO7",
                        "commonName": "Waterloo Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.502858702770006,
                        "lon": -0.11381867113000001
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G000401",
                        "platformName": "E",
                        "stopLetter": "E",
                        "icsCode": "1003705",
                        "individualStopId": "490000254E",
                        "commonName": "Waterloo Station   / Waterloo Road",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.503512433190004,
                        "lon": -0.11141418974
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.50287679539, -0.11384148749],[51.50288498506, -0.11382551714],[51.50301918783, -0.11365483724],[51.50327640869, -0.11334941004],[51.50325404172, -0.11330449428],[51.50326522520, -0.11329551113],[51.50327081695, -0.11327754482],[51.50336587648, -0.11345720788],[51.50342738548, -0.11337635950],[51.50343856892, -0.11341229211],[51.50358395347, -0.11333144374],[51.50372933755, -0.11328652797],[51.50411516229, -0.11300805023],[51.50409838737, -0.11295415132],[51.50408720408, -0.11289126925],[51.50403128762, -0.11258584205],[51.50401451267, -0.11244211160],[51.50403128762, -0.11243312845],[51.50402569597, -0.11241516215],[51.50402010432, -0.11238821269],[51.50401451267, -0.11236126323],[51.50400892102, -0.11232533062],[51.50394182114, -0.11207380234],[51.50393063782, -0.11205583603],[51.50394741280, -0.11201990342],[51.50391386283, -0.11197498766],[51.50388031284, -0.11185820667],[51.50378525438, -0.11173244253],[51.50374052092, -0.11167854361],[51.50351126125, -0.11141803218]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "name": "Waterloo Station / Waterloo Road",
                                "uri": "/StopPoint/",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "99",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T12:06:00",
                    "scheduledArrivalTime": "2025-02-11T12:13:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 2,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "188 bus to The Old Vic",
                        "detailed": "188 bus towards North Greenwich Station",
                        "steps": []
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T12:13:00",
                    "arrivalTime": "2025-02-11T12:15:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G000401",
                        "platformName": "E",
                        "stopLetter": "E",
                        "icsCode": "1003705",
                        "individualStopId": "490000254E",
                        "commonName": "Waterloo Station   / Waterloo Road",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.503512433190004,
                        "lon": -0.11141418974
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G00013485",
                        "platformName": "",
                        "stopLetter": "S",
                        "icsCode": "1013485",
                        "individualStopId": "490013485S1",
                        "commonName": "The Old Vic",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.50133829726,
                        "lon": -0.10875208244
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.50351326990, -0.11142164451],[51.50349110085, -0.11139619592],[51.50341302973, -0.11130028998],[51.50330892591, -0.11119047549],[51.50326928586, -0.11114687053],[51.50320856619, -0.11107863351],[51.50311556261, -0.11097686221],[51.50308151099, -0.11093965458],[51.50300837576, -0.11084873332],[51.50297769492, -0.11080864878],[51.50281433802, -0.11060446000],[51.50274636384, -0.11053248998],[51.50253835916, -0.11028649177],[51.50252809931, -0.11027481289],[51.50248302523, -0.11022884067],[51.50245586481, -0.11014495304],[51.50241461019, -0.11009046598],[51.50239602868, -0.11007019809],[51.50233944053, -0.11000726812],[51.50221676031, -0.10987200404],[51.50215965840, -0.10981068076],[51.50211499866, -0.10976253093],[51.50206472610, -0.10971763925],[51.50197597952, -0.10963457221],[51.50193510059, -0.10964245952],[51.50171846501, -0.10937996892],[51.50155415103, -0.10918908607],[51.50139893010, -0.10900445601],[51.50134080372, -0.10893539679],[51.50129111210, -0.10887636256],[51.50113521566, -0.10871121373],[51.50108209603, -0.10864036307]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "490G00013485",
                                "name": "The Old Vic",
                                "uri": "/StopPoint/490G00013485",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "188",
                            "directions": [
                                "North Greenwich Station"
                            ],
                            "lineIdentifier": {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "188",
                                "name": "188",
                                "uri": "/Line/188",
                                "type": "Line",
                                "crowding": {
                                    "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
                                },
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            "direction": "Inbound"
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "bus",
                        "name": "bus",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "3",
                        "network": "tfl"
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T12:13:00",
                    "scheduledArrivalTime": "2025-02-11T12:15:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 10,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to SE1 0RB",
                        "detailed": "Walk to SE1 0RB",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "Waterloo Road for 93 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Waterloo Road",
                                "distance": 93,
                                "cumulativeDistance": 93,
                                "skyDirection": 324,
                                "skyDirectionDescription": "NorthWest",
                                "cumulativeTravelTime": 83,
                                "latitude": 51.50128623545,
                                "longitude": -0.10886950436000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Gray Street/Webber Street, continue for 135 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Gray Street/Webber Street",
                                "distance": 135,
                                "cumulativeDistance": 229,
                                "skyDirection": 320,
                                "skyDirectionDescription": "NorthWest",
                                "cumulativeTravelTime": 205,
                                "latitude": 51.500616979259995,
                                "longitude": -0.10807594724,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Valentine Place, continue for 164 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Valentine Place",
                                "distance": 164,
                                "cumulativeDistance": 393,
                                "skyDirection": 216,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 353,
                                "latitude": 51.50121497638,
                                "longitude": -0.10668239296,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Cycle Superhighway 6, continue for 17 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Cycle Superhighway 6",
                                "distance": 17,
                                "cumulativeDistance": 411,
                                "skyDirection": 280,
                                "skyDirectionDescription": "West",
                                "cumulativeTravelTime": 368,
                                "latitude": 51.50174097688,
                                "longitude": -0.10472985759,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Pocock Street, continue for 129 metres",
                                "turnDirection": "RIGHT",
                                "streetName": "Pocock Street",
                                "distance": 129,
                                "cumulativeDistance": 540,
                                "skyDirection": 182,
                                "skyDirectionDescription": "South",
                                "cumulativeTravelTime": 485,
                                "latitude": 51.501902734569995,
                                "longitude": -0.1047231464,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn right",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Rushworth Street, continue for 123 metres",
                                "turnDirection": "SLIGHT_RIGHT",
                                "streetName": "Rushworth Street",
                                "distance": 123,
                                "cumulativeDistance": 663,
                                "skyDirection": 260,
                                "skyDirectionDescription": "West",
                                "cumulativeTravelTime": 596,
                                "latitude": 51.502070638350006,
                                "longitude": -0.10287188244,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Take a slight right",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T12:15:00",
                    "arrivalTime": "2025-02-11T12:25:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "490G00013485",
                        "platformName": "",
                        "stopLetter": "S",
                        "icsCode": "1013485",
                        "individualStopId": "490013485S1",
                        "commonName": "The Old Vic",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.50133829726,
                        "lon": -0.10875208244
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.Place, Tfl.Api.Presentation.Entities",
                        "commonName": "SE1 0RB",
                        "placeType": "StopPoint",
                        "lat": 51.501251032750005,
                        "lon": -0.10168121278
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.50128623545, -0.10886950436],[51.50113090977, -0.10871744347],[51.50108481592, -0.10864731051],[51.50102051669, -0.10856352322],[51.50097488722, -0.10852218779],[51.50086495838, -0.10839706567],[51.50076401597, -0.10827157201],[51.50073635951, -0.10822949282],[51.50069971648, -0.10818778583],[51.50061697926, -0.10807594724],[51.50083699715, -0.10777867179],[51.50096923984, -0.10761470374],[51.50126874117, -0.10722768069],[51.50129523605, -0.10719776627],[51.50132149852, -0.10715345310],[51.50128276341, -0.10698215825],[51.50122419538, -0.10669641918],[51.50121497638, -0.10668239296],[51.50125045766, -0.10665210580],[51.50127695238, -0.10662219106],[51.50170938837, -0.10611438020],[51.50176717816, -0.10579499784],[51.50180629616, -0.10543316356],[51.50181295651, -0.10528880242],[51.50179172645, -0.10508796418],[51.50174097688, -0.10472985759],[51.50190273457, -0.10472314640],[51.50190939404, -0.10457878487],[51.50191628606, -0.10444882217],[51.50192108313, -0.10418926961],[51.50193626291, -0.10401573724],[51.50197770360, -0.10379788906],[51.50201541823, -0.10334965821],[51.50207063835, -0.10287188244],[51.50119874505, -0.10178424373],[51.50125103275, -0.10168121278]]",
                        "stopPoints": [],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "100",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "distance": 663.0,
                    "isDisrupted": false,
                    "hasFixedLocations": false,
                    "scheduledDepartureTime": "2025-02-11T12:15:00",
                    "scheduledArrivalTime": "2025-02-11T12:25:00"
                }
            ]
        },
        {
            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Journey, Tfl.Api.Presentation.Entities",
            "startDateTime": "2025-02-11T11:33:00",
            "duration": 55,
            "arrivalDateTime": "2025-02-11T12:28:00",
            "alternativeRoute": false,
            "legs": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 15,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to Golders Green Station",
                        "detailed": "Walk to Golders Green Station",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "Ravenscroft Avenue for 161 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Ravenscroft Avenue",
                                "distance": 161,
                                "cumulativeDistance": 161,
                                "skyDirection": 43,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 145,
                                "latitude": 51.57592562195,
                                "longitude": -0.20105195994,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Golders Green Road, continue for 398 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Golders Green Road",
                                "distance": 398,
                                "cumulativeDistance": 560,
                                "skyDirection": 42,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 503,
                                "latitude": 51.574852864979995,
                                "longitude": -0.20263847656,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Golders Green Road, continue for 55 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Golders Green Road",
                                "distance": 55,
                                "cumulativeDistance": 615,
                                "skyDirection": 295,
                                "skyDirectionDescription": "NorthWest",
                                "cumulativeTravelTime": 552,
                                "latitude": 51.572502513879996,
                                "longitude": -0.19831539989,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Golders Green Road/Finchley Road/North End Road, continue for 203 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Golders Green Road/Finchley Road/North End Road",
                                "distance": 203,
                                "cumulativeDistance": 818,
                                "skyDirection": 299,
                                "skyDirectionDescription": "NorthWest",
                                "cumulativeTravelTime": 734,
                                "latitude": 51.572284520290005,
                                "longitude": -0.1975880581,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 49 metres",
                                "turnDirection": "LEFT",
                                "streetName": "",
                                "distance": 49,
                                "cumulativeDistance": 867,
                                "skyDirection": 289,
                                "skyDirectionDescription": "West",
                                "cumulativeTravelTime": 798,
                                "latitude": 51.571720496009995,
                                "longitude": -0.19482529413,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "for 7 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "",
                                "distance": 7,
                                "cumulativeDistance": 874,
                                "skyDirection": 277,
                                "skyDirectionDescription": "West",
                                "cumulativeTravelTime": 804,
                                "latitude": 51.57202161277,
                                "longitude": -0.19452475479,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000087,
                            "position": "IDEST"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000087,
                            "position": "IDEST"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000087,
                            "position": "IDEST"
                        }
                    ],
                    "departureTime": "2025-02-11T11:33:00",
                    "arrivalTime": "2025-02-11T11:48:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "platformName": "",
                        "icsCode": "99999997",
                        "commonName": "NW11 8AU",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57605497606,
                        "lon": -0.20127776128
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUGGN",
                        "platformName": "",
                        "icsCode": "1000087",
                        "individualStopId": "9400ZZLUGGN2",
                        "commonName": "Golders Green Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57242047478,
                        "lon": -0.1941481846
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57605497606, -0.20127776128],[51.57592562195, -0.20105195994],[51.57549498969, -0.20170395398],[51.57485286498, -0.20263847656],[51.57452970641, -0.20208840308],[51.57448366697, -0.20201806327],[51.57445560132, -0.20194701431],[51.57433523544, -0.20172086417],[51.57426112991, -0.20157947660],[51.57398378542, -0.20108533336],[51.57391910826, -0.20097243786],[51.57379896167, -0.20076071532],[51.57364109778, -0.20043503514],[51.57342909033, -0.20009706495],[51.57324470640, -0.19980129923],[51.57316205421, -0.19968911754],[51.57308816756, -0.19956215904],[51.57293162825, -0.19932302050],[51.57283011654, -0.19915386265],[51.57276521623, -0.19902655075],[51.57268167791, -0.19885668371],[51.57254089705, -0.19847261982],[51.57250251388, -0.19831539989],[51.57247444604, -0.19824435633],[51.57228474180, -0.19760247994],[51.57227949544, -0.19758628749],[51.57228210691, -0.19760240054],[51.57226535709, -0.19754850162],[51.57215369150, -0.19714425974],[51.57210344190, -0.19694663038],[51.57209227531, -0.19691069777],[51.57206435883, -0.19678493363],[51.57203085904, -0.19659628742],[51.57199735922, -0.19644357382],[51.57194152613, -0.19619204554],[51.57192477619, -0.19609323086],[51.57191919287, -0.19594051726],[51.57187452633, -0.19561712376],[51.57185777636, -0.19551830908],[51.57180752643, -0.19520389873],[51.57171819308, -0.19482660631],[51.57174052644, -0.19480864000],[51.57176285978, -0.19479965685],[51.57176844311, -0.19482660631],[51.57176844311, -0.19483558946],[51.57182985974, -0.19479965685],[51.57187452633, -0.19477270739],[51.57193035950, -0.19473677478],[51.57192477619, -0.19468287586],[51.57198060930, -0.19464694325],[51.57203085904, -0.19461999379],[51.57202527573, -0.19452117911],[51.57200294252, -0.19441338128],[51.57200279544, -0.19442308749],[51.57234813584, -0.19412219015],[51.57244719544, -0.19411808749]]",
                        "stopPoints": [],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "100",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "distance": 615.0,
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:33:00",
                    "scheduledArrivalTime": "2025-02-11T11:48:00",
                    "interChangeDuration": "5",
                    "interChangePosition": "IDEST"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 25,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Northern line to Borough",
                        "detailed": "Northern line towards Morden via Bank",
                        "steps": []
                    },
                    "obstacles": [],
                    "departureTime": "2025-02-11T11:48:00",
                    "arrivalTime": "2025-02-11T12:13:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUGGN",
                        "platformName": "",
                        "icsCode": "1000087",
                        "individualStopId": "9400ZZLUGGN2",
                        "commonName": "Golders Green Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.57242047478,
                        "lon": -0.1941481846
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUBOR",
                        "platformName": "",
                        "icsCode": "1000026",
                        "individualStopId": "9400ZZLUBOR2",
                        "commonName": "Borough Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.5009225342,
                        "lon": -0.09362625743
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.57244721319, -0.19411807483],[51.57243097918, -0.19405945266],[51.57238106907, -0.19387816152],[51.57221672562, -0.19327887911],[51.57209026276, -0.19268127327],[51.57197369951, -0.19204936620],[51.57189356230, -0.19161068395],[51.57183410377, -0.19127104128],[51.57176615517, -0.19088238438],[51.57163553036, -0.19024310797],[51.57151008380, -0.18961329780],[51.57140845156, -0.18913420754],[51.57131209473, -0.18887468340],[51.57125235373, -0.18868037283],[51.57112867500, -0.18817142739],[51.57108816868, -0.18794749316],[51.57092126580, -0.18727764246],[51.57069597614, -0.18648414503],[51.57050600020, -0.18583470445],[51.57022767638, -0.18500249657],[51.56996618128, -0.18434004526],[51.56962746305, -0.18359208039],[51.56939005344, -0.18312088920],[51.56915820346, -0.18271268299],[51.56894742554, -0.18241099649],[51.56864321431, -0.18196989928],[51.56842355504, -0.18172773449],[51.56822308289, -0.18155738602],[51.56800770788, -0.18141764662],[51.56534518889, -0.18013817553],[51.56473311550, -0.17989136293],[51.56397765176, -0.17965865156],[51.56319407879, -0.17949791058],[51.56237043060, -0.17937974956],[51.56152518247, -0.17932997461],[51.56018830767, -0.17936634408],[51.55909850573, -0.17945242483],[51.55879112089, -0.17952038564],[51.55847528177, -0.17965201438],[51.55816049343, -0.17975864201],[51.55795358378, -0.17975319825],[51.55774838565, -0.17968998203],[51.55750530400, -0.17955557214],[51.55734565503, -0.17943168086],[51.55712655761, -0.17921452115],[51.55700556375, -0.17886390143],[51.55670459950, -0.17843016867],[51.55661549441, -0.17829178000],[51.55654375823, -0.17817394577],[51.55654375823, -0.17817394577],[51.55651389686, -0.17812489549],[51.55642738257, -0.17797385414],[51.55633487726, -0.17780184718],[51.55627866619, -0.17769128574],[51.55601358095, -0.17741409223],[51.55587465053, -0.17692802660],[51.55560045243, -0.17601836367],[51.55542790008, -0.17536559710],[51.55518137958, -0.17431679460],[51.55481941309, -0.17287117733],[51.55447671606, -0.17189001668],[51.55364712826, -0.17002440230],[51.55324920156, -0.16925697052],[51.55300527015, -0.16878657075],[51.55236280262, -0.16764875890],[51.55170850454, -0.16662353005],[51.55131407582, -0.16598352753],[51.55077217389, -0.16510815798],[51.55052275471, -0.16478240827],[51.55040627441, -0.16462482746],[51.55040627441, -0.16462482746],[51.55036869131, -0.16457398326],[51.55022370262, -0.16437658907],[51.55001910537, -0.16408798646],[51.54956178063, -0.16345214854],[51.54891531397, -0.16218297251],[51.54864556333, -0.16171946432],[51.54759897948, -0.16011037598],[51.54718631418, -0.15927896703],[51.54667930218, -0.15802303202],[51.54641562700, -0.15731760424],[51.54619185577, -0.15679416916],[51.54599566191, -0.15640634833],[51.54568082315, -0.15584477991],[51.54442977517, -0.15388812616],[51.54422637948, -0.15351510984],[51.54422637948, -0.15351510984],[51.54420180134, -0.15347003528],[51.54369297002, -0.15220537760],[51.54349069904, -0.15156979241],[51.54331082088, -0.15088888677],[51.54294143462, -0.14900859983],[51.54270180102, -0.14787572172],[51.54244552083, -0.14709584285],[51.54216140464, -0.14643838580],[51.54186006810, -0.14585230007],[51.54141259721, -0.14517496657],[51.54086287055, -0.14440619581],[51.54049393438, -0.14396435689],[51.53997926607, -0.14347942596],[51.53954625749, -0.14307467555],[51.53930268349, -0.14284662026],[51.53930268349, -0.14284662026],[51.53927069065, -0.14281666598],[51.53905908868, -0.14262296484],[51.53893021736, -0.14252582854],[51.53886735645, -0.14248584855],[51.53879171847, -0.14244537950],[51.53870802723, -0.14241879337],[51.53859611696, -0.14239898016],[51.53849036131, -0.14236464063],[51.53840296759, -0.14232003639],[51.53820816190, -0.14214786382],[51.53794492086, -0.14193579706],[51.53565239526, -0.13947437898],[51.53537316812, -0.13920156595],[51.53519240948, -0.13906489224],[51.53505367242, -0.13900927025],[51.53493846154, -0.13897417316],[51.53478422038, -0.13894456129],[51.53460498658, -0.13893802976],[51.53431951470, -0.13896885026],[51.53274536282, -0.13909807761],[51.53249656747, -0.13907708062],[51.53227866411, -0.13904775914],[51.53160630670, -0.13887837504],[51.53133158807, -0.13880480284],[51.53066350707, -0.13854225788],[51.52910641137, -0.13766116456],[51.52881471333, -0.13743576478],[51.52860402957, -0.13723820158],[51.52839555351, -0.13695318408],[51.52831007490, -0.13682548058],[51.52817409072, -0.13649036405],[51.52808567570, -0.13596848429],[51.52805895714, -0.13542462336],[51.52808747311, -0.13503492733],[51.52814121354, -0.13465948158],[51.52821373973, -0.13430618962],[51.52832803101, -0.13388198814],[51.52844536426, -0.13354733290],[51.52857701044, -0.13318541921],[51.52867954339, -0.13284602474],[51.52867954339, -0.13284602474],[51.52878749531, -0.13248868775],[51.52904617283, -0.13167319890],[51.52930150690, -0.13099249358],[51.52942771444, -0.13070172077],[51.52974516015, -0.12999149879],[51.52994849405, -0.12954113135],[51.53009160341, -0.12916574829],[51.53023389676, -0.12871110046],[51.53038863577, -0.12819682764],[51.53049273202, -0.12760288180],[51.53056540604, -0.12694476728],[51.53068154954, -0.12511286130],[51.53070958327, -0.12438578422],[51.53071132082, -0.12434260422],[51.53074378487, -0.12345992227],[51.53078510403, -0.12236681006],[51.53081618083, -0.12189158503],[51.53081618083, -0.12189158503],[51.53093541846, -0.12006792881],[51.53100106842, -0.11907530603],[51.53103706738, -0.11859486631],[51.53142181793, -0.11363138281],[51.53185438856, -0.10927095264],[51.53189210019, -0.10790660194],[51.53188982863, -0.10721953481],[51.53185132750, -0.10654449612],[51.53182152646, -0.10613006264],[51.53178477233, -0.10592355228],[51.53178477233, -0.10592355228],[51.53174072716, -0.10567607887],[51.53165407080, -0.10532167933],[51.53148756826, -0.10472289803],[51.53146990265, -0.10465918391],[51.52969716785, -0.09776261920],[51.52803729977, -0.09117917490],[51.52737091322, -0.08872479725],[51.52701922855, -0.08821245835],[51.52669706845, -0.08795579012],[51.52563668314, -0.08754307967],[51.52544559343, -0.08752875534],[51.52544559343, -0.08752875534],[51.52540970351, -0.08752606500],[51.52532137769, -0.08751938649],[51.52433377897, -0.08744544211],[51.52221487570, -0.08700504876],[51.52169258763, -0.08700502605],[51.52066236948, -0.08716855937],[51.51978142139, -0.08724900299],[51.51951442056, -0.08732548594],[51.51914857395, -0.08748913373],[51.51889769361, -0.08764808021],[51.51889769361, -0.08764808021],[51.51851200143, -0.08789243364],[51.51717937091, -0.08862481005],[51.51537349666, -0.08936512761],[51.51456442597, -0.08967368642],[51.51427286705, -0.08963933236],[51.51353521749, -0.08921491170],[51.51339225443, -0.08913326815],[51.51299595893, -0.08887429376],[51.51221178423, -0.08831072740],[51.51221178423, -0.08831072740],[51.51212635399, -0.08824933212],[51.51197490678, -0.08815479041],[51.51126843560, -0.08772363204],[51.51090988012, -0.08746310081],[51.51075254093, -0.08731058904],[51.51050709858, -0.08718713253],[51.50990281817, -0.08714427888],[51.50936685165, -0.08709409733],[51.50926563508, -0.08708551128],[51.50911569861, -0.08705057664],[51.50873036377, -0.08686294970],[51.50858929271, -0.08680919912],[51.50844337598, -0.08677813243],[51.50827771724, -0.08677167041],[51.50714208815, -0.08711061733],[51.50695377610, -0.08719286075],[51.50676428781, -0.08732429113],[51.50661277410, -0.08749591933],[51.50605242981, -0.08823396783],[51.50585241228, -0.08849739332],[51.50555221575, -0.08890982552],[51.50555221575, -0.08890982552],[51.50438862725, -0.09050837831],[51.50407139949, -0.09095766310],[51.50381428966, -0.09121105881],[51.50327927507, -0.09163369727],[51.50309747997, -0.09177399848],[51.50270149745, -0.09204240618],[51.50198272838, -0.09245194910],[51.50176227660, -0.09262065683],[51.50129931089, -0.09314427972],[51.50109358975, -0.09340602052],[51.50093647439, -0.09364805248]]",
                        "stopPoints": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUHTD",
                                "name": "Hampstead Underground Station",
                                "uri": "/StopPoint/940GZZLUHTD",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBZP",
                                "name": "Belsize Park Underground Station",
                                "uri": "/StopPoint/940GZZLUBZP",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCFM",
                                "name": "Chalk Farm Underground Station",
                                "uri": "/StopPoint/940GZZLUCFM",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUCTN",
                                "name": "Camden Town Underground Station",
                                "uri": "/StopPoint/940GZZLUCTN",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUEUS",
                                "name": "Euston Underground Station",
                                "uri": "/StopPoint/940GZZLUEUS",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUKSX",
                                "name": "King's Cross St. Pancras Underground Station",
                                "uri": "/StopPoint/940GZZLUKSX",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUAGL",
                                "name": "Angel Underground Station",
                                "uri": "/StopPoint/940GZZLUAGL",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUODS",
                                "name": "Old Street Underground Station",
                                "uri": "/StopPoint/940GZZLUODS",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUMGT",
                                "name": "Moorgate Underground Station",
                                "uri": "/StopPoint/940GZZLUMGT",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBNK",
                                "name": "Bank Underground Station",
                                "uri": "/StopPoint/940GZZLUBNK",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLULNB",
                                "name": "London Bridge Underground Station",
                                "uri": "/StopPoint/940GZZLULNB",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "940GZZLUBOR",
                                "name": "Borough Underground Station",
                                "uri": "/StopPoint/940GZZLUBOR",
                                "type": "StopPoint",
                                "routeType": "Unknown",
                                "status": "Unknown"
                            }
                        ],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "Northern",
                            "directions": [
                                "Morden via Bank"
                            ],
                            "lineIdentifier": {
                                "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                                "id": "northern",
                                "name": "Northern",
                                "uri": "/Line/northern",
                                "type": "Line",
                                "crowding": {
                                    "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
                                },
                                "routeType": "Unknown",
                                "status": "Unknown"
                            },
                            "direction": "Inbound"
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "tube",
                        "name": "tube",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "1",
                        "network": "tfl"
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "isDisrupted": false,
                    "hasFixedLocations": true,
                    "scheduledDepartureTime": "2025-02-11T11:48:00",
                    "scheduledArrivalTime": "2025-02-11T12:13:00"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Leg, Tfl.Api.Presentation.Entities",
                    "duration": 15,
                    "instruction": {
                        "$type": "Tfl.Api.Presentation.Entities.Instruction, Tfl.Api.Presentation.Entities",
                        "summary": "Walk to SE1 0RB",
                        "detailed": "Walk to SE1 0RB",
                        "steps": [
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "Borough High Street for 3 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Borough High Street",
                                "distance": 3,
                                "cumulativeDistance": 3,
                                "skyDirection": 225,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 2,
                                "latitude": 51.50094050716,
                                "longitude": -0.0936255074,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Borough High Street, continue for 13 metres",
                                "turnDirection": "SLIGHT_LEFT",
                                "streetName": "Borough High Street",
                                "distance": 13,
                                "cumulativeDistance": 16,
                                "skyDirection": 225,
                                "skyDirectionDescription": "SouthWest",
                                "cumulativeTravelTime": 14,
                                "latitude": 51.50095824607,
                                "longitude": -0.09361035890000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Take a slight left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Borough High Street, continue for 193 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Borough High Street",
                                "distance": 193,
                                "cumulativeDistance": 209,
                                "skyDirection": 22,
                                "skyDirectionDescription": "North",
                                "cumulativeTravelTime": 187,
                                "latitude": 51.501064913520004,
                                "longitude": -0.09353386611,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Great Suffolk Street, continue for 260 metres",
                                "turnDirection": "RIGHT",
                                "streetName": "Great Suffolk Street",
                                "distance": 260,
                                "cumulativeDistance": 469,
                                "skyDirection": 47,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 421,
                                "latitude": 51.49990199473,
                                "longitude": -0.09557068825000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn right",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Webber Street/Rushworth Street, continue for 209 metres",
                                "turnDirection": "LEFT",
                                "streetName": "Webber Street/Rushworth Street",
                                "distance": 209,
                                "cumulativeDistance": 679,
                                "skyDirection": 38,
                                "skyDirectionDescription": "NorthEast",
                                "cumulativeTravelTime": 609,
                                "latitude": 51.501007847400004,
                                "longitude": -0.09888171012000001,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Turn left",
                                "trackType": "None"
                            },
                            {
                                "$type": "Tfl.Api.Presentation.Entities.InstructionStep, Tfl.Api.Presentation.Entities",
                                "description": "on to Rushworth Street, continue for 28 metres",
                                "turnDirection": "STRAIGHT",
                                "streetName": "Rushworth Street",
                                "distance": 28,
                                "cumulativeDistance": 707,
                                "skyDirection": 143,
                                "skyDirectionDescription": "SouthEast",
                                "cumulativeTravelTime": 634,
                                "latitude": 51.50099684624,
                                "longitude": -0.10153328478,
                                "pathAttribute": {
                                    "$type": "Tfl.Api.Presentation.Entities.PathAttribute, Tfl.Api.Presentation.Entities"
                                },
                                "descriptionHeading": "Continue along ",
                                "trackType": "None"
                            }
                        ]
                    },
                    "obstacles": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "STAIRS",
                            "incline": "UP",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        },
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Obstacle, Tfl.Api.Presentation.Entities",
                            "type": "WALKWAY",
                            "incline": "LEVEL",
                            "stopId": 1000026,
                            "position": "BEFORE"
                        }
                    ],
                    "departureTime": "2025-02-11T12:13:00",
                    "arrivalTime": "2025-02-11T12:28:00",
                    "departurePoint": {
                        "$type": "Tfl.Api.Presentation.Entities.StopPoint, Tfl.Api.Presentation.Entities",
                        "naptanId": "940GZZLUBOR",
                        "platformName": "",
                        "icsCode": "1000026",
                        "individualStopId": "9400ZZLUBOR2",
                        "commonName": "Borough Underground Station",
                        "placeType": "StopPoint",
                        "additionalProperties": [],
                        "lat": 51.5009225342,
                        "lon": -0.09362625743
                    },
                    "arrivalPoint": {
                        "$type": "Tfl.Api.Presentation.Entities.Place, Tfl.Api.Presentation.Entities",
                        "commonName": "SE1 0RB",
                        "placeType": "StopPoint",
                        "lat": 51.501251032750005,
                        "lon": -0.10168121278
                    },
                    "path": {
                        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.Path, Tfl.Api.Presentation.Entities",
                        "lineString": "[[51.50093900055, -0.09363138955],[51.50096136866, -0.09360444009],[51.50106202502, -0.09353257487],[51.50106849539, -0.09352908749],[51.50106491352, -0.09353386611],[51.50095824607, -0.09361035890],[51.50082672548, -0.09381756225],[51.50075647180, -0.09392135095],[51.50069543852, -0.09403916280],[51.50059064262, -0.09423084069],[51.50038175165, -0.09465738874],[51.50017285908, -0.09508393291],[51.50000679289, -0.09537901631],[51.49998053492, -0.09542333483],[51.49996326343, -0.09546727866],[51.49994599192, -0.09551122246],[51.49990199473, -0.09557068825],[51.49996747205, -0.09572644590],[51.49998661400, -0.09579768766],[51.50001497618, -0.09588295312],[51.50006224634, -0.09602506245],[51.50010928259, -0.09615277386],[51.50017522660, -0.09633732956],[51.50030898312, -0.09682162898],[51.50037609428, -0.09707817809],[51.50041367566, -0.09717746911],[51.50044250407, -0.09729153292],[51.50049922622, -0.09746206755],[51.50050891347, -0.09750488839],[51.50059516388, -0.09783268325],[51.50079228681, -0.09834316992],[51.50081119372, -0.09840001562],[51.50083932058, -0.09847088579],[51.50084900746, -0.09851370718],[51.50088635420, -0.09859860194],[51.50093315426, -0.09871191983],[51.50096104751, -0.09876839187],[51.50098018763, -0.09883963649],[51.50100784740, -0.09888171012],[51.50098158811, -0.09892602765],[51.50092860266, -0.09898586554],[51.50092008295, -0.09901503652],[51.50090257671, -0.09904458143],[51.50089475714, -0.09911694789],[51.50087013135, -0.09926205464],[51.50086207829, -0.09932002252],[51.50080407283, -0.09962500777],[51.50078061289, -0.09984210633],[51.50074746623, -0.10001638304],[51.50069961161, -0.10039298524],[51.50070031128, -0.10043618060],[51.50069412328, -0.10060933567],[51.50069738790, -0.10081091401],[51.50070018586, -0.10098369548],[51.50071197010, -0.10115610344],[51.50072258850, -0.10125651916],[51.50074079467, -0.10127017061],[51.50075876771, -0.10126942359],[51.50076775423, -0.10126905008],[51.50078596039, -0.10128270155],[51.50099684624, -0.10153328478],[51.50118975853, -0.10178461714],[51.50125103275, -0.10168121278]]",
                        "stopPoints": [],
                        "elevation": []
                    },
                    "routeOptions": [
                        {
                            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.RouteOption, Tfl.Api.Presentation.Entities",
                            "name": "",
                            "directions": [
                                ""
                            ],
                            "direction": ""
                        }
                    ],
                    "mode": {
                        "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
                        "id": "walking",
                        "name": "walking",
                        "type": "Mode",
                        "routeType": "Unknown",
                        "status": "Unknown",
                        "motType": "100",
                        "network": ""
                    },
                    "disruptions": [],
                    "plannedWorks": [],
                    "distance": 691.0,
                    "isDisrupted": false,
                    "hasFixedLocations": false,
                    "scheduledDepartureTime": "2025-02-11T12:13:00",
                    "scheduledArrivalTime": "2025-02-11T12:28:00",
                    "interChangeDuration": "5",
                    "interChangePosition": "BEFORE"
                }
            ]
        }
    ],
    "lines": [
        {
            "$type": "Tfl.Api.Presentation.Entities.Line, Tfl.Api.Presentation.Entities",
            "id": "13",
            "name": "13",
            "modeName": "bus",
            "disruptions": [],
            "created": "2025-02-06T09:58:47.417Z",
            "modified": "2025-02-06T09:58:47.417Z",
            "lineStatuses": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineStatus, Tfl.Api.Presentation.Entities",
                    "id": 0,
                    "statusSeverity": 10,
                    "statusSeverityDescription": "Good Service",
                    "created": "0001-01-01T00:00:00",
                    "validityPeriods": []
                }
            ],
            "routeSections": [],
            "serviceTypes": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo, Tfl.Api.Presentation.Entities",
                    "name": "Regular",
                    "uri": "/Line/Route?ids=13&serviceTypes=Regular"
                }
            ],
            "crowding": {
                "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
            }
        },
        {
            "$type": "Tfl.Api.Presentation.Entities.Line, Tfl.Api.Presentation.Entities",
            "id": "188",
            "name": "188",
            "modeName": "bus",
            "disruptions": [],
            "created": "2025-02-06T09:58:47.4Z",
            "modified": "2025-02-06T09:58:47.4Z",
            "lineStatuses": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineStatus, Tfl.Api.Presentation.Entities",
                    "id": 0,
                    "statusSeverity": 10,
                    "statusSeverityDescription": "Good Service",
                    "created": "0001-01-01T00:00:00",
                    "validityPeriods": []
                }
            ],
            "routeSections": [],
            "serviceTypes": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo, Tfl.Api.Presentation.Entities",
                    "name": "Regular",
                    "uri": "/Line/Route?ids=188&serviceTypes=Regular"
                }
            ],
            "crowding": {
                "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
            }
        },
        {
            "$type": "Tfl.Api.Presentation.Entities.Line, Tfl.Api.Presentation.Entities",
            "id": "240",
            "name": "240",
            "modeName": "bus",
            "disruptions": [],
            "created": "2025-02-06T09:58:47.4Z",
            "modified": "2025-02-06T09:58:47.4Z",
            "lineStatuses": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineStatus, Tfl.Api.Presentation.Entities",
                    "id": 0,
                    "statusSeverity": 10,
                    "statusSeverityDescription": "Good Service",
                    "created": "0001-01-01T00:00:00",
                    "validityPeriods": []
                }
            ],
            "routeSections": [],
            "serviceTypes": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo, Tfl.Api.Presentation.Entities",
                    "name": "Regular",
                    "uri": "/Line/Route?ids=240&serviceTypes=Regular"
                }
            ],
            "crowding": {
                "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
            }
        },
        {
            "$type": "Tfl.Api.Presentation.Entities.Line, Tfl.Api.Presentation.Entities",
            "id": "northern",
            "name": "Northern",
            "modeName": "tube",
            "disruptions": [],
            "created": "2025-02-06T09:58:47.4Z",
            "modified": "2025-02-06T09:58:47.4Z",
            "lineStatuses": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineStatus, Tfl.Api.Presentation.Entities",
                    "id": 0,
                    "statusSeverity": 10,
                    "statusSeverityDescription": "Good Service",
                    "created": "0001-01-01T00:00:00",
                    "validityPeriods": []
                }
            ],
            "routeSections": [],
            "serviceTypes": [
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo, Tfl.Api.Presentation.Entities",
                    "name": "Regular",
                    "uri": "/Line/Route?ids=Northern&serviceTypes=Regular"
                },
                {
                    "$type": "Tfl.Api.Presentation.Entities.LineServiceTypeInfo, Tfl.Api.Presentation.Entities",
                    "name": "Night",
                    "uri": "/Line/Route?ids=Northern&serviceTypes=Night"
                }
            ],
            "crowding": {
                "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
            }
        }
    ],
    "stopMessages": [],
    "recommendedMaxAgeMinutes": 0,
    "searchCriteria": {
        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.SearchCriteria, Tfl.Api.Presentation.Entities",
        "dateTime": "2025-02-11T11:28:00",
        "dateTimeType": "Departing",
        "timeAdjustments": {
            "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustments, Tfl.Api.Presentation.Entities",
            "earliest": {
                "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustment, Tfl.Api.Presentation.Entities",
                "date": "20250211",
                "time": "0300",
                "timeIs": "departing",
                "uri": "/journey/journeyresults/%7bnw118au%7d/to/%7bse10rb%7d?app_key=b1efe66db0f748c3a9a248ca9ed03c9b&app_id=2e21963ed6f645da8fa40ef78065949d&time=0300&date=20250211&timeIs=departing"
            },
            "earlier": {
                "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustment, Tfl.Api.Presentation.Entities",
                "date": "20250211",
                "time": "1113",
                "timeIs": "departing",
                "uri": "/journey/journeyresults/%7bnw118au%7d/to/%7bse10rb%7d?app_key=b1efe66db0f748c3a9a248ca9ed03c9b&app_id=2e21963ed6f645da8fa40ef78065949d&time=1113&date=20250211&timeIs=departing"
            },
            "later": {
                "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustment, Tfl.Api.Presentation.Entities",
                "date": "20250211",
                "time": "1134",
                "timeIs": "departing",
                "uri": "/journey/journeyresults/%7bnw118au%7d/to/%7bse10rb%7d?app_key=b1efe66db0f748c3a9a248ca9ed03c9b&app_id=2e21963ed6f645da8fa40ef78065949d&time=1134&date=20250211&timeIs=departing"
            },
            "latest": {
                "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.TimeAdjustment, Tfl.Api.Presentation.Entities",
                "date": "20250212",
                "time": "0300",
                "timeIs": "departing",
                "uri": "/journey/journeyresults/%7bnw118au%7d/to/%7bse10rb%7d?app_key=b1efe66db0f748c3a9a248ca9ed03c9b&app_id=2e21963ed6f645da8fa40ef78065949d&time=0300&date=20250212&timeIs=departing"
            }
        }
    },
    "journeyVector": {
        "$type": "Tfl.Api.Presentation.Entities.JourneyPlanner.JourneyVector, Tfl.Api.Presentation.Entities",
        "from": "{NW118au}",
        "to": "{SE10RB}",
        "via": "",
        "uri": "/journey/journeyresults/%7bnw118au%7d/to/%7bse10rb%7d?app_key=b1efe66db0f748c3a9a248ca9ed03c9b&app_id=2e21963ed6f645da8fa40ef78065949d"
    }
}