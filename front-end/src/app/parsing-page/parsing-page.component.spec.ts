import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ParsingPageComponent } from './parsing-page.component';

describe('ParsingPageComponent', () => {
  let component: ParsingPageComponent;
  let fixture: ComponentFixture<ParsingPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ParsingPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ParsingPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
