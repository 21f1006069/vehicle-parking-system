select 
pl.lot_id, 
pl.address,
Count(Case WHEN ps.status = 'A' THEN 1 END) As availabilty 
from ParkingLot PL 
Left Join 
ParkingSpots PS ON PL.lot_id = PS.lot_id
Group By
PL.lot_id,PL.address