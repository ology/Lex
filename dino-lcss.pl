#!/usr/bin/env perl
use strict;
use warnings;

use Data::Dumper::Compact 'ddc';
use List::Util 'uniq';
use Storable;
use String::LCSS 'lcss';

my $word = shift || '';
my $count_thresh = shift || 1;
my $length_thresh = shift || 1;
my $max = shift || 50;
my $match = shift || '';

my $frag_file = 'fragments.dat';

print "Collecting words...\n";
my @words;
while (my $line = readline(DATA)) {
    chomp $line;
    push @words, lc $line;
}

my %frags;
if (-e $frag_file) {
    %frags = %{ retrieve($frag_file) };
}
else {
    print "Building fragments...\n";
    for my $i (@words) {
        for my $j (@words) {
            next if $i eq $j;
            my $lcss = lcss($i, $j);
            if ($lcss) {
                my $key;
                my $jpos = index $j, $lcss;
                if ($jpos == 0) {
                    $key = '^' . $lcss;
                }
                elsif ($jpos == length($j) - length($lcss)) {
                    $key = $lcss . '$';
                }
                else {
                    $key = '(?<=\w)' . $lcss . '(?=\w)';
                }
                $frags{$lcss}{count}++;
                push @{ $frags{$lcss}{text} }, $key;
                push @{ $frags{$lcss}{regex} }, qr/$key/;
            }
        }
    }
    for my $fragment (sort keys %frags) {
        $frags{$fragment}{text} = [ uniq @{ $frags{$fragment}{text} }];
        $frags{$fragment}{regex} = [ uniq @{ $frags{$fragment}{regex} }];
    }
#warn(__PACKAGE__,' ',__LINE__," MARK: ",ddc(\%frags));exit;
    store(\%frags, $frag_file);
}

print "Prune fragments...\n";
for my $fragment (sort keys %frags) {
    delete $frags{$fragment}
        if length $fragment < $length_thresh || $frags{$fragment}{count} < $count_thresh;
}
#warn(__PACKAGE__,' ',__LINE__," MARK: ",ddc(\%frags));exit;

#print "Creating a fragment file...\n";
#$file = $ENV{HOME} . '/Documents/data/dino-fragments.txt';
#open $fh, '>', $file or die "Can't write $file: $!";
#print $fh "$_\n" for uniq sort keys %frags;
#close $fh;exit;

if ($word) {
    print "Computing knowns...\n";
    my %by_pos;
    for my $fragment (sort keys %frags) {
        for my $re (@{ $frags{$fragment}{regex} }) {
            while ($word =~ /$re/g) {
                push @{ $by_pos{"@-"} }, $fragment;
            }
        }
    }
warn(__PACKAGE__,' ',__LINE__," MARK: ",ddc(\%by_pos));
}

print "Build names...\n";
my (@heads, @mids, @tails);
for my $fragment (keys %frags) {
    for my $text (@{ $frags{$fragment}{text} }) {
        if ($text =~ /\^/) {
            push @heads, $fragment;
        }
        elsif ($text =~ /\$/) {
            push @tails, $fragment;
        }
        else {
            push @mids, $fragment;
        }
    }
}

if ($match) {
    push @heads, $match;
    push @mids, $match;
}

for my $i (1 .. $max) {
    my $name = $heads[int rand @heads] . $mids[int rand @mids] . $tails[int rand @tails];
    print "$i. $name\n" if !$match || $name =~ /$match/;
}

__DATA__
Aardonyx
Abelisaurus
Abrictosaurus
Abrosaurus
Acanthopholis
Achillobator
Acrocanthosaurus
Adamantisaurus
Adasaurus
Adeopapposaurus
Aegyptosaurus
Aeolosaurus
Agilisaurus
Agujaceratops
Agustinia
Ajkaceratops
Alamosaurus
Alaskacephale
Albalophosaurus
Albertaceratops
Albertadromeus
Albertonykus
Albertosaurus
Aletopelta
Alioramus
Allosaurus
Altirhinus
Alwalkeria
Amargasaurus
Amazonsaurus
Amphicoelias
Amurosaurus
Anabisetia
Anatotitan
Anchisaurus
Andesaurus
Angaturama
Angolatitan
Angulomastacator
Animantarx
Ankylosaurus
Anodontosaurus
Anserimimus
Antarctopelta
Antarctosaurus
Antetonitrus
Aorun
Apatosaurus
Aquilops
Aralosaurus
Archaeoceratops
Archaeopteryx
Archaeornithomimus
Arcovenator
Arcusaurus
Argentinosaurus
Argyrosaurus
Aristosuchus
Arrhinoceratops
Astrodon
Asylosaurus
Atlasaurus
Atlascopcosaurus
Atrociraptor
Aublysodon
Aucasaurus
Auroraceratops
Australodocus
Australovenator
Austrosaurus
Avaceratops
Aviatyrannis
Avimimus
Bactrosaurus
Bagaceratops
Bagaraatan
Bahariasaurus
Bambiraptor
Barosaurus
Barsboldia
Baryonyx
Batyrosaurus
Becklespinax
Beipiaosaurus
Beishanlong
Bellusaurus
Berberosaurus
Bistahieversor
Borogovia
Bothriospondylus
Brachiosaurus
Brachyceratops
Brachylophosaurus
Bravoceratops
Bruhathkayosaurus
Buitreraptor
Camarasaurus
Camelotia
Carcharodontosaurus
Carnotaurus
Caudipteryx
Centrosaurus
Cerasinops
Ceratonykus
Ceratosaurus
Cetiosauriscus
Changyuraptor
Chaoyangsaurus
Chasmosaurus
Chialingosaurus
Chilantaisaurus
Chindesaurus
Chubutisaurus
Chungkingosaurus
Citipati
Coahuilaceratops
Coelophysis
Colepiocephale
Compsognathus
Concavenator
Conchoraptor
Condorraptor
Coronosaurus
Corythosaurus
Crichtonsaurus
Cruxicheiros
Cryolophosaurus
Cryptovolans
Cumnoria
Dacentrurus
Dahalokely
Daspletosaurus
Deinocheirus
Deinodon
Deinonychus
Delapparentia
Deltadromeus
Demandasaurus
Diamantinasaurus
Diceratops
Dicraeosaurus
Dilophosaurus
Dimetrodon
Diplodocus
Dollodon
Draconyx
Dracopelta
Dracorex
Dreadnoughtus
Drinker
Dromaeosauroides
Dromiceiomimus
Dryosaurus
Dubreuillosaurus
Duriavenator
Dyoplosaurus
Dysalotosaurus
Dyslocosaurus
Echinodon
Edmarka
Edmontonia
Edmontosaurus
Efraasia
Einiosaurus
Ekrixinatosaurus
Elaphrosaurus
Elmisaurus
Elopteryx
Elrhazosaurus
Enigmosaurus
Eoabelisaurus
Eobrontosaurus
Eocarcharia
Eocursor
Eodromaeus
Eolambia
Eoraptor
Eotriceratops
Eotyrannus
Epachthosaurus
Epidendrosaurus
Equijubus
Erectopus
Erketu
Erliansaurus
Erlikosaurus
Euhelopus
Euoplocephalus
Europasaurus
Europelta
Euskelosaurus
Eustreptospondylus
Fabrosaurus
Ferganasaurus
Fruitadens
Fukuiraptor
Fukuisaurus
Futalognkosaurus
Gallimimus
Gargoyleosaurus
Gasosaurus
Gasparinisaura
Genyodectes
Gideonmantellia
Giganotosaurus
Gigantoraptor
Gigantspinosaurus
Gilmoreosaurus
Giraffatitan
Glacialisaurus
Gobiceratops
Gobisaurus
Gobivenator
Gondwanatitan
Gorgosaurus
Goyocephale
Graciliraptor
Gryphoceratops
Gryponyx
Gryposaurus
Guaibasaurus
Guanlong
Hadrosaurus
Hagryphus
Haplocanthosaurus
Haplocheirus
Harpymimus
Haya
Herrerasaurus
Hesperonychus
Hesperosaurus
Hexing
Hexinlusaurus
Heyuannia
Hippodraco
Homalocephale
Hongshanosaurus
Hoplitosaurus
Huabeisaurus
Huanghetitan
Huaxiagnathus
Huaxiaosaurus
Huayangosaurus
Huehuecanauhtlus
Hungarosaurus
Huxleysaurus
Hypselosaurus
Hypselospinus
Hypsibema
Hypsilophodon
Ignavusaurus
Iguanacolossus
Iguanodon
Ilokelesia
Indosuchus
Ingenia
Isanosaurus
Isisaurus
Jainosaurus
Jaxartosaurus
Jeholosaurus
Jianchangosaurus
Jinfengopteryx
Jingshanosaurus
Jinzhousaurus
Jobaria
Judiceratops
Juratyrant
Juravenator
Kaijiangosaurus
Kazaklambia
Kerberosaurus
Khaan
Kileskus
Kinnareemimus
Kol
Koreanosaurus
Kosmoceratops
Kotasaurus
Kritosaurus
Kryptops
Kukufeldia
Kundurosaurus
Lagosuchus
Lambeosaurus
Lanzhousaurus
Laosaurus
Lapparentosaurus
Laquintasaura
Latirhinus
Leaellynasaura
Leonerasaurus
Leshansaurus
Lesothosaurus
Lessemsaurus
Lexovisaurus
Leyesaurus
Liaoningosaurus
Liliensternus
Limaysaurus
Limusaurus
Linhenykus
Linheraptor
Linhevenato -r
Lophorhothon
Loricatosaurus
Lourinhanosaurus
Luanchuanraptor
Lufengosaurus
Lurdusaurus
Lusotitan
Lycorhinus
Lythronax
Machairasaurus
Macrogryphosaurus
Magnapaulia
Magnirostris
Magnosaurus
Magyarosaurus
Mahakala
Maiasaura
Majungasaurus
Malawisaurus
Mamenchisaurus
Manidens
Mantellodon
Mapusaurus
Marshosaurus
Masiakasaurus
Massospondylus
Maxakalisaurus
Megalosaurus
Megapnosaurus
Megaraptor
Mei
Melanorosaurus
Mendozasaurus
Mercuriceratops
Metriacanthosaurus
Microceratops
Micropachycephalosaurus
Microraptor
Minmi
Minotaurasaurus
Miragaia
Mirischia
Mochlodon
Mojoceratops
Monoclonius
Monolophosaurus
Montanoceratops
Mussaurus
Muttaburrasaurus
Nankangia
Nanotyrannus
Nanshiungosaurus
Nanyangosaurus
Nasutoceratops
Nebulasaurus
Neimongosaurus
Nemegtosaurus
Neovenator
Neuquenraptor
Neuquensaurus
Nigersaurus
Nipponosaurus
Nqwebasaurus
Nuthetes
Nyasasaurus
Ojoceratops
Omeisaurus
Oohkotokia
Opisthocoelicaudia
Ornitholestes
Ornithomimus
Ornithopsis
Orodromeus
Orthomerus
Ostafrikasaurus
Othnielia
Othnielosaurus
Ouranosaurus
Overosaurus
Oviraptor
Oxalaia
Ozraptor
Pachycephalosaurus
Pachyrhinosaurus
Palaeoscincus
Pamparaptor
Panamericansaurus
Panoplosaurus
Panphagia
Paralititan
Paranthodon
Pararhabdodon
Parasaurolophus
Parvicursor
Patagosaurus
Pedopenna
Pegomastax
Peloroplites
Pentaceratops
Philovenator
Phuwiangosaurus
Piatnitzkysaurus
Pisanosaurus
Piveteausaurus
Planicoxa
Plateosaurus
Pneumatoraptor
Podokesaurus
Poekilopleuron
Polacanthus
Prenocephale
Prenoceratops
Proa
Probactrosaurus
Proceratosaurus
Procompsognathus
Prosaurolophus
Protarchaeopteryx
Protoceratops
Protohadros
Psittacosaurus
Puertasaurus
Pyroraptor
Qantassaurus
Qianzhousaurus
Qiaowanlong
Qiupalong
Quaesitosaurus
Rahiolisaurus
Rajasaurus
Raptorex
Rebbachisaurus
Regnosaurus
Rhabdodon
Richardoestesia
Rinchenia
Rinconsaurus
Riojasaurus
Sahaliyania
Saltasaurus
Saltopus
Sanjuansaurus
Sarcolestes
Saturnalia
Saurophaganax
Sauroposeidon
Saurornithoides
Scelidosaurus
Scolosaurus
Scutellosaurus
Secernosaurus
Seismosaurus
Seitaad
Sellosaurus
Shamosaurus
Shanag
Shenzhousaurus
Shuvuuia
Siamodon
Siamosaurus
Siamotyrannus
Sigilmassasaurus
Sinocalliopteryx
Sinornithoides
Sinornithomimus
Sinornithosaurus
Sinovenator
Sinusonasus
Skorpiovenator
Sonorasaurus
Sphaerotholus
Spinophorosaurus
Spinosaurus
Spinostropheus
Stegoceras
Stegosaurus
Struthiomimus
Struthiosaurus
Stygimoloch
Styracosaurus
Suchomimus
Sulaimanisaurus
Supersaurus
Suzhousaurus
Tachiraptor
Talarurus
Talenkauen
Talos
Tangvayosaurus
Tanius
Tanycolagreus
Taohelong
Tapuiasaurus
Tarascosaurus
Tarbosaurus
Tarchia
Tastavinsaurus
Tatankacephalus
Tatankaceratops
Tataouinea
Tawa
Tazoudasaurus
Tehuelchesaurus
Tenontosaurus
Texacephale
Thecocoelurus
Theiophytalia
Therizinosaurus
Tianyulong
Tianzhenosaurus
Titanosaurus
Triceratops
Troodon
Tuojiangosaurus
Turiasaurus
Tylocephale
Tyrannosaurus Rex
Uberabatitan
Udanoceratops
Unaysaurus
Unescoceratops
Urbacodon
Utahraptor
Uteodon
Vagaceratops
Vahiny
Valdoraptor
Valdosaurus
Variraptor
Velafrons
Wannanosaurus
Wellnhoferia
Wendiceratops
Wintonotitan
Wuerhosaurus
Wulagasaurus
Xenoposeidon
Xenotarsosaurus
Xiaosaurus
Xiaotingia
Xiongguanlong
Xixianykus
Xuanhuaceratops
Xuwulong
Yamaceratops
Yandusaurus
Yangchuanosaurus
Yimenosaurus
Yinlong
Yongjinglong
Yulong
Yunnanosaurus
Yutyrannus
Zby
Zhenyuanlong
Zhongyuansaurus
Zhuchengceratops
Zhuchengosaurus
Zuolong
Zupaysaurus
