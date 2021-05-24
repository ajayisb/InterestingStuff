T=readtable('/home/iiti/Downloads/Datastreams/stationary/auto93.csv');
     %       ^^^^^^^^^------ your csv filename
p=T{:,1:23};
save('/home/iiti/Downloads/Datastreams/stationary/mymat.mat','p')
  %   ^^^^^^^^^----- your resulting .mat filename   